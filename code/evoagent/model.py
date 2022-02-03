"""
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""
import shutil
from evoagent.utils import *
from mesa.time import BaseScheduler
from collections import namedtuple
import numpy as np
from mesa import Model
import pathlib
import neat
from evoagent.evoagent import Countdown
import pickle
import os
from tqdm.auto import tqdm
import sty
from itertools import count

class FoodToken():
    radius = 5

    def __init__(self, pos, energy, model, respawn_after=100):
        self.pos = pos
        self.energy = energy
        self.model = model
        self.respawn_after = respawn_after
        self.eaten = False
        self.countdown_respawn = Countdown(self.respawn_after)

    def get_eaten(self):
        self.eaten = True
        self.pos = np.array([-10.0, -10.0])
        if self.respawn_after < np.inf:
            self.countdown_respawn.start()


    def step(self):
        self.countdown_respawn.step()
        if self.countdown_respawn.counter == 0 and self.eaten:
            self.pos = self.model.get_random_coord()
            self.eaten = False


class MyRandomActivation(BaseScheduler):
    def step(self) -> None:
        for idx, agent in enumerate(self.agent_buffer(shuffled=False)):
            agent.step(idx)
        self.steps += 1
        self.time += 1

class Environment(Model):
    """
    Flocker model class. Handles agent creation, placement and scheduling.
    """
    global_id = 0
    selected_agent_unique_id = 0
    previous_epoch = None
    running = True
    step_start_epoch = 0
    message = ''
    socket_message = None
    extinct = False

    def __init__(
            self,
            initial_population=100,
            epochs=None,
            size=None,
            name_run='sim',
            pop=None,  # either a path or an array of pop
            server_model=None,
            reset_on_extinction=False,
            **kwargs
    ):
        self.reset_on_extinction = reset_on_extinction
        self.server_model = server_model
        self.step_count = 0
        self.all_food = []
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  './config-feedforward')
        self.initial_pop = initial_population
        self.max_size = np.array(size) if size else np.array([100, 100])
        self.schedule = MyRandomActivation(self)
        self.name_run = name_run
        self.saved_model_folder = f'./data/{self.name_run}/save_model/'
        self.saved_pop_folder = f'./data/{self.name_run}/save_pop/'

        self.net_svg_folder = f'./data/{self.name_run}/nets_svg/'
        self.all_epochs = epochs
        self.pbar = tqdm(total=np.sum([e.duration for e in self.all_epochs]), dynamic_ncols=True, colour="yellow")

        self.current_epoch = self.all_epochs.popleft()
        shutil.rmtree(self.net_svg_folder) if os.path.exists(self.net_svg_folder) else None
        pathlib.Path(self.saved_model_folder).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.saved_pop_folder).mkdir(parents=True, exist_ok=True)

        pathlib.Path(self.net_svg_folder).mkdir(parents=True, exist_ok=True)
        self.spawn_food()
        self.make_agents(pop)

        ## Here we update the GLOBAL node indexer so that it never overlaps with those already used in the loaded pops (useful when the loaded pop is a mixture of pops coming from different simulations)
        if pop is not None:
            l = [list(a.genome.nodes.keys()) for a in self.schedule.agents]
            flat_l = [e for l in l for e in l]  # flatten list of lists... not sure htf it does that.
            self.config.genome_config.node_indexer = count(max(flat_l) +1)

        self.previous_epoch = None
        self.running = True
        self.save_model_state()
        print(f"RUN: {self.name_run}")

    def spawn_food(self):
        self.all_food = [FoodToken(self.get_random_coord(), e, self) for e in self.current_epoch.energy_list]

    def make_agents(self, pop=None):
        if pop is not None:
            if isinstance(pop, str):
                pop = pickle.load(open(pop, 'rb'))
            self.global_id = pop[0].model.global_id
            for a in pop:
                self.schedule.add(a)
                a.model = self
        else:
            for i in range(self.initial_pop):
                self.spawn_agent()
        self.selected_agent_unique_id = self.schedule.agents[0].unique_id

    def save_model_state(self):
        server_cmd = self.server_model  # this object can't be pickled..
        self.server_model = None
        pbar_cmd = self.pbar
        self.pbar = None
        pickle.dump(self, open(self.saved_model_folder + f'/step{self.step_count}.pickle', 'wb'))
        pickle.dump([i for i in self.schedule.agents], open(self.saved_pop_folder + f'/step{self.step_count}.pickle', 'wb'))
        self.message += 'saved in: ' + self.saved_model_folder + f'/step{self.step_count}.pickle\n'
        self.server_model = server_cmd
        self.pbar = pbar_cmd

    def stop(self):
        self.server_model.event_loop.stop() if self.server_model is not None else None
        self.server_model = None
        tqdm._instances.pop().close()

        print("Epochs finished!")
        self.message += 'epochs finished\n'
        self.running = False
        self.save_model_state()
        return "Finished"

    def step(self):
        self.pbar.set_description("Steps")
        self.pbar.set_postfix_str(f"n. pop {len(self.schedule.agents)}")
        self.pbar.update(1)
        print(sty.rs.fg, end="")
        # if self.step_count % 50 == 0:
        #     print(f"Step: {self.step_count}, n pop: {len(self.schedule.agents)}")
        self.step_count += 1
        self.message = ''

        if self.step_count % 1000 == 0:
            self.save_model_state()

        if self.step_count - self.step_start_epoch >= self.current_epoch.duration:
            if len(self.all_epochs) == 0:
                return self.stop()
            self.message += f'step {self.step_count}: new epoch'
            self.step_start_epoch = self.step_count
            self.current_epoch = self.all_epochs.popleft()
            print(self.message)
            self.spawn_food()

        if len(self.schedule.agents) > 0:
            self.food_dist_matrix = np.linalg.norm(np.array([[i.pos - j.pos for i in self.all_food] for j in self.schedule.agents]), axis=2)
        self.schedule.step()
        for f in self.all_food:
            f.step()

        if len(self.schedule.agents) == 0:
            if self.reset_on_extinction:
                self.pbar.disable = True
                print("Extinctiong. Restarting") if not self.extinct else None
                self.extinct = True
                self.socket_message = "reset"
                tqdm._instances.pop().close()
                return "Extinction"
            else:
                self.server_model.event_loop.stop() if self.server_model is not None else None
        return "Step"

    def create_new_genome(self, genome_type, genome_config):
        g = genome_type(self.global_id)
        g.configure_new(genome_config)
        return g

    def get_random_coord(self):
        x = self.random.random() * self.max_size[0]
        y = self.random.random() * self.max_size[1]
        return np.array([x, y])

    def spawn_agent(self, pos=None, dir=None, genome=None, parent=None):
        from .evoagent import EvoAgent
        if pos is None:
            pos = self.get_random_coord()
        dir = np.random.uniform(0, 2 * np.pi) if dir is None else dir
        agent = EvoAgent(
            self.global_id,
            self,
            pos,
            dir,
            genome=self.create_new_genome(self.config.genome_type, self.config.genome_config) if genome is None else genome,
            parent=parent
        )


        self.global_id += 1
        self.schedule.add(agent)



