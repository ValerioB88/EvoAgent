from mesa.visualization.ModularVisualization import ModularServer
from evoagent.utils import *
from evoagent.SimpleContinuousModule import SimpleCanvas
from evoagent.network_chart import PopChart
from matplotlib import colors

size = (1000, 1000)

name_run = "load_difficult_env_pop"


pop_loaded = "difficult_envS0"
evo_canvas = SimpleCanvas(*size, name_run, f'pop_loaded: ./data/{pop_loaded}/save_pop/step10000.pickle')

epochs = deque([Epoch(10000, [0.8]*200)])

model_params = {
    # "pop": f"./data/{pop_loaded}/save_pop/step1000.pickle",  # test a population with a new model.
    "pop": pickle.load(open("./data/difficult_envS0/save_pop/step10000.pickle", 'rb')),  # you can also pass the list of agents directly
    "initial_population": 50,
    "epochs": epochs,
    "size": size,
    "name_run": name_run
}
pop_chart = PopChart([name_run], render_with_canvas=False, plot_every=10)

server = ModularServer(model_factory, [input_chart, output_chart, evo_canvas, pop_chart], "EvoAgent", model_params, verbose=False)
server.launch(8651)
