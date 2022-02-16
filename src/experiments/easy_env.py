from mesa.mesa.visualization.ModularVisualization import ModularServer
from src.evoagent.utils import *
from src.evoagent.SimpleContinuousModule import SimpleCanvas
from src.evoagent.network_chart import PopChart
from copy import deepcopy


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


def run(seed=0, test=False, env_view=False):
    size = (1000, 1000)

    name_run = f"easy_envS{seed}"

    if test:
        epochs = deque([Epoch(2000, [0.8] * 200)])
        pop = f'./data/{name_run}/save_pop/step10000.pickle'
        collect_data = True
        additional_info = f'Pop: {pop}'
    else:
        epochs = deque([Epoch(2000, [0.8]*200),
                        Epoch(2000, [0.8]*100),
                        Epoch(6000, [0.8]*75)])
        pop = None
        collect_data = False
        additional_info = ''

    model_params = {
        "initial_population": 50,
        "epochs": epochs,
        "size": size,
        "name_run": name_run,
        "reset_on_extinction": True,
        "pop": pop,
        "collect_data": collect_data
    }

    run_model(model_params, env_view=env_view, modules=[input_chart,
                                                    output_chart,
                                                    SimpleCanvas(*size, name_run, additional_info=additional_info),
                                                    PopChart([name_run], render_with_canvas=False, plot_every=10)
                                                    ])

if __name__ == '__main__':
    run()