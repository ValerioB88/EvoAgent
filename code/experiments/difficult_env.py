from mesa.visualization.ModularVisualization import ModularServer
from evoagent.utils import *
from evoagent.SimpleContinuousModule import SimpleCanvas
from evoagent.network_chart import PopChart

size = (1000, 1000)

name_run = "difficult_envS0"

evo_canvas = SimpleCanvas(*size, name_run)

epochs = deque([Epoch(2000, [0.8]*200),
                Epoch(2000, [0.8]*100),
                Epoch(6000, [0.8]*75)])

model_params = {
    "initial_population": 50,
    "epochs": epochs,
    "size": size,
    "name_run": name_run
}

pop_chart = PopChart([name_run], render_with_canvas=False, plot_every=10)

server = ModularServer(model_factory, [input_chart, output_chart, evo_canvas, pop_chart], "EvoAgent", model_params, verbose=False)
server.launch(8657)

stop=1

