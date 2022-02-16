from mesa.mesa.visualization.ModularVisualization import ModularServer
from src.evoagent.utils import *
from src.evoagent.SimpleContinuousModule import SimpleCanvas
from src.evoagent.network_chart import PopChart
from matplotlib import colors


size = (1000, 1000)

name_run = "easy_env"
load_model_file = './data/easy_envS0/save_model/step1000.pickle'

evo_canvas = SimpleCanvas(*size, name_run, f"Model Loaded: {load_model_file}")

epochs = deque([Epoch(10000, [0.8]*200)])  # this will be ignored. We are loading the state of the previous simulation

model_params = {
    "model_path": load_model_file,  ##  Note that in this case all the other given parameters will be ignored!
    "initial_population": 50,
    "epochs": epochs,
    "size": size,
    "name_run": name_run
}

pop_chart = PopChart([name_run], render_with_canvas=False, plot_every=10)

server = ModularServer(model_factory, [input_chart, output_chart, evo_canvas, pop_chart], "EvoAgent", model_params, verbose=False)
server.launch(8641)