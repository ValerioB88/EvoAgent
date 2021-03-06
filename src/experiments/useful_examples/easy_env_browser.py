from src.evoagent.utils import *
from src.evoagent.SimpleContinuousModule import SimpleCanvas
from src.evoagent.network_chart import PopChart
from mesa.visualization.ModularVisualization import ModularServer
from collections import deque

def run(seed=0):
    size = (1000, 1000)

    name_run = f"easy_envS{seed}"

    epochs = deque([Epoch(10000, [0.8]*200)])
    model_params = {
        "initial_population": 50,
        "epochs": epochs,
        "size": size,
        "name_run": name_run,
        "reset_on_extinction": True,
    }



    evo_canvas = SimpleCanvas(*size, name_run)
    pop_chart = PopChart([name_run], render_with_canvas=False, plot_every=10)
    #
    server = ModularServer(model_factory, [input_chart, output_chart, evo_canvas, pop_chart], "EvoAgent", model_params, verbose=False)
    server.launch()

if __name__ == '__main__':
    run()