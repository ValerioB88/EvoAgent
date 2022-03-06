from mesa.mesa.visualization.ModularVisualization import ModularServer
from collections import namedtuple, deque
import pickle
from .model import Environment
from .network_chart import InputChart, OutputChart
from matplotlib import colors
from copy import deepcopy

Epoch = namedtuple('Epoch', ['duration', 'energy_list'])

def model_factory(model_path=None, *args, **kwargs):
    if model_path:
        model_factory.model = pickle.load(open(model_path, 'rb'))
    else:
        model_factory.model = Environment(*args, **kwargs)
    return model_factory.model

def find_pop_idx_from_id(agents, id):
    for idx, a in enumerate(agents):
        if a.unique_id == id:
            break
    return idx

def run_model(model_params, env_view=False, modules=None):
    if env_view:
        server = ModularServer(model_factory, modules, "EvoAgent", model_params, verbose=False)
        server.launch()
    else:
        r = "Start"
        while r != "Finished":
            m = model_factory(**deepcopy(model_params))
            r = m.step()
            while r == "Step":
                r = m.step()


input_chart = InputChart(
    [{"Label": "Energy", "Color": colors.to_hex("red")},
     {"Label": "Fdist", "Color": colors.to_hex("green")},
     {"Label": "Frad", "Color": colors.to_hex("yellow")}]
)

output_chart = OutputChart(
    [{"Label": "Forward", "Color": colors.to_hex("red")},
     {"Label": "Rotation", "Color": colors.to_hex("green")}])
