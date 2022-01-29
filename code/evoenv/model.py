"""
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""
from evoenv.utils import *

from collections import namedtuple
import numpy as np
from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from datetime import datetime
import pathlib
import neat
from evoenv.visualize import draw_net
from evoenv.evoagent import Countdown
class FoodToken():
    radius = 5
    _rad = 0
    _dist = 0

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




from mesa.time import BaseScheduler
class MyRandomActivation(BaseScheduler):
    def step(self) -> None:
        for idx, agent in enumerate(self.agent_buffer(shuffled=False)):
            agent.step(idx)
        self.steps += 1
        self.time += 1

from typing import Deque
class Environment(Model):
    """
    Flocker model class. Handles agent creation, placement and scheduling.
    """
    global_id = 0

    def __init__(
            self,
            initial_population=100,
            epochs: Deque[Epoch] =None,
            space_width=100,
            space_height=100,
    ):
        self.all_food = []
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  './config-feedforward')
        self.population = initial_population
        self.max_size = np.array([space_width, space_height])
        self.schedule = MyRandomActivation(self)
        self.make_agents()
        self.all_epochs = epochs
        self.selected_agent_unique_id = self.schedule.agents[0].unique_id
        self.current_epoch = self.all_epochs.popleft()
        self.spawn_food()
        self.step_count = 0
        # self.update_food_tokens(self.current_epoch.num_good_food, self.current_epoch.num_bad_food)
        self.previous_epoch = None
        self.running = True

    def spawn_food(self):
        self.all_food = [FoodToken(self.get_random_coord(), e, self) for e in self.current_epoch.energy_list]


    def make_agents(self):
        for i in range(self.population):
            self.spawn_agent()

    def step(self):
        if len(self.all_epochs) > 0 and self.step_count > self.all_epochs[0].init_step:
            self.current_epoch = self.all_epochs.popleft()
            self.spawn_food()

        if len(self.schedule.agents) > 0:
            self.food_dist_matrix = np.linalg.norm(np.array([[i.pos - j.pos for i in self.all_food] for j in self.schedule.agents]), axis=2)
        # import evoenv.visualize as vis
        self.schedule.step()
        for f in self.all_food:
            f.step()

        self.step_count += 1

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
        agent.spawn()
        self.global_id += 1
        # self.space.place_agent(agent, pos)
        self.schedule.add(agent)



