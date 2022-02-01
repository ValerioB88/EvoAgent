import numpy as np
from mesa import Agent
import string
import random
import numpy as np
import neat


class CountdownList():
    def __init__(self, cdl=None):
        self.countdown_list = cdl if cdl is not None else []

    def add(self, countdown):
        self.countdown_list.append(countdown)

    def step(self):
        for i in self.countdown_list:
            i.step()

class Countdown():
    counter = np.inf
    started = False

    def __init__(self, max=100, autostart=False, callback=None):
        self.max = max
        self.autostart = autostart
        self.callback = callback

    def start(self):
        self.started = True
        self.counter = self.max

    def step(self):
        if self.started:
            self.counter -= 1
            if self.counter < 0:
                if self.autostart:
                    self.counter = self.max
                else:
                    self.counter = 0
                    self.callback() if self.callback is not None else None
                    self.started = False
        return self.counter


class EvoAgent(Agent):

    age = 0

    fov = np.pi / 1.5
    max_vision_dist = 100
    energy_depletion = 0.008
    radius = 5
    max_speed_forward = 5  # in px/time steps
    max_speed_rotation = 5  # in dg/time steps
    max_age = 500
    time_between_children = 100
    fertile_age_start = 90
    num_children = 0
    fertile = False

    target_food = -1

    def __init__(
        self,
        unique_id,
        model,
        pos,
        direction,
        genome,
        parent: 'EvoAgent' =None
    ):
        super().__init__(unique_id, model)
        if parent is not None:
            self.parent_id = parent.unique_id
            self.surname = parent.surname
            self.generation = parent.generation + 1
            self.color_hsl = np.clip(parent.color_hsl + np.random.randint(-5, 5), 0, 255)
            self.name_run = parent.name_run
        else:
            self.color_hsl = np.random.randint(0, 256)
            self.generation = 0
            self.parent_id = []
            self.surname = ''.join(random.choices(string.ascii_lowercase, k=5))
            self.name_run = self.model.name_run

        self.name = ''.join(random.choices(string.ascii_lowercase, k=5))

        self.inputs = []
        self.outputs = []
        self.children_id = []
        self.pos = pos
        self.direction = direction
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, self.model.config)
        self.countdown_offspring = Countdown(self.time_between_children)
        self.countdown_list = CountdownList([self.countdown_offspring])
        self.energy = 1 # np.random.uniform(0.75, 1)
        # self.network_svg_path = self.model.data_folder + f'/nets/net_{self.unique_id}'
        self.network_drawn = False


    def compute_vision(self, pop_idx):

        close_food_idx = np.where(self.model.food_dist_matrix[pop_idx] < self.max_vision_dist)[0]
        close_food = [self.model.all_food[i] for i in np.where(self.model.food_dist_matrix[pop_idx] < self.max_vision_dist)[0]]
        if len(close_food):
            # import warnings
            # warnings.filterwarnings("error")

            ag_view = np.array([np.cos(self.direction), np.sin(self.direction)])
            # try:
            #     print("HERE")
            #     print(ag_view)
            #     [print(np.dot(ag_view, (self.model.all_food[i].pos - self.pos)) / (np.linalg.norm(ag_view) * self.model.food_dist_matrix[pop_idx][i])) for i in close_food_idx]
            all_rads = [ np.arccos(np.dot(ag_view, (self.model.all_food[i].pos - self.pos)) / (np.linalg.norm(ag_view) * self.model.food_dist_matrix[pop_idx][i])) for i in close_food_idx]
            # except RuntimeWarning:
            #
            #     stop=1

            in_range_idx = [(all_rads[idx], i) for idx, i in enumerate(close_food_idx) if all_rads[idx] < self.fov/2 ]
            if in_range_idx:
                rad, selected_food_idx = in_range_idx[np.argmin([self.model.food_dist_matrix[pop_idx][i[1]] for i in in_range_idx])]
                s = np.sign(np.cross(ag_view, (self.model.all_food[selected_food_idx].pos - self.pos)))
                rad *= s
                return self.model.food_dist_matrix[pop_idx][selected_food_idx], rad, selected_food_idx

        return self.max_vision_dist, 0, -1

    def step(self, pop_idx):
        self.energy -= self.energy_depletion

        dist, rad, self.target_food = self.compute_vision(pop_idx)
        d_input = (self.max_vision_dist - dist)/self.max_vision_dist
        rad_input = rad / (self.fov / 2)
        self.inputs = [self.energy, d_input, rad_input]
        out_forward, out_rotation = np.array(self.net.activate(self.inputs)) * [self.max_speed_forward, self.max_speed_rotation]
        self.outputs = [out_forward, out_rotation]
        self.pos = np.array([self.pos[0] + np.cos(self.direction)*out_forward, self.pos[1] + np.sin(self.direction)*out_forward])
        self.direction += np.deg2rad(out_rotation)


        [self.eat_food(self.model.all_food[i]) for i in np.where(self.model.food_dist_matrix[pop_idx] < self.radius * 2)[0]]


        if self.age > self.fertile_age_start and not self.fertile:
            self.fertile = True
            self.countdown_offspring.start()

        if self.age > self.fertile_age_start and (self.countdown_offspring.counter == 0 or self.countdown_offspring.counter == np.inf):
            self.reproduce_asexual()

        # bounce against walls
        if (self.pos[0] > self.model.max_size[0] - self.radius) or (self.pos[1] > self.model.max_size[1] - self.radius) or (self.pos[0] < 0 + self.radius) or (self.pos[1] < 0 + self.radius):
            self.pos = np.array([np.clip(self.pos[0], 0 + self.radius, self.model.max_size[0] - self.radius), np.clip(self.pos[1], 0 + self.radius, self.model.max_size[1] - self.radius)])

        if self.age > self.max_age or self.energy < 0:
            self.die()
        self.countdown_list.step()
        self.age += 1

    def eat_food(self, food):
        self.energy = np.clip(self.energy + food.energy, 0, 1)
        food.get_eaten()


    def die(self):
        self.model.schedule.remove(self)
        if len(self.model.schedule.agents) > 0:
            if self.unique_id == self.model.selected_agent_unique_id:
                self.model.selected_agent_unique_id = self.model.schedule.agents[np.argmin(np.abs([i.unique_id - self.model.selected_agent_unique_id for i in self.model.schedule.agents]))].unique_id

    def find_partner(self):
        pass
        # find reproductive parnet

    def reproduce_asexual(self):
        new_genome = self.model.config.genome_type(self.model.global_id)
        for key, cg1 in self.genome.connections.items():
            new_genome.connections[key] = cg1.copy()

        for key, cg1 in self.genome.nodes.items():
            new_genome.nodes[key] = cg1.copy()


        new_genome.mutate(self.model.config.genome_config)
        self.children_id.append(self.model.global_id)
        self.model.spawn_agent(self.pos, dir=None, genome=new_genome, parent=self)
        self.countdown_offspring.start()
        self.num_children += 1

