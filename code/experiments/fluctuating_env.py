from mesa.visualization.ModularVisualization import ModularServer
from evoagent.utils import *
from evoagent.SimpleContinuousModule import SimpleCanvas
from evoagent.network_chart import PopChart
from copy import deepcopy

def run(seed=0):
    size = (1000, 1000)

    name_run = f"fluctuating_envS{seed}"

    evo_canvas = SimpleCanvas(*size, name_run)

    epochs = deque([Epoch(2000, [0.8]*200),
                    Epoch(1000, [0.8]*100),
                    Epoch(1000, [0.8]*75),
                    Epoch(1000, [0.8]*200),
                    Epoch(1000, [0.8]*75),
                    Epoch(1000, [0.8]*200),
                    Epoch(1000, [0.8]*75),
                    Epoch(1000, [0.8]*200),
                    Epoch(1000, [0.8]*75)])

    model_params = {
        "initial_population": 50,
        "epochs": epochs,
        "size": size,
        "name_run": name_run,
        "reset_on_extinction": True,
    }

    r = "Start"
    while r != "Finished":
        m = model_factory(**deepcopy(model_params))
        r = m.step()
        while r == "Step":
            r = m.step()


if __name__ == '__main__':
    run()