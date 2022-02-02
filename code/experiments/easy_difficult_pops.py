
import pickle
from mesa.visualization.ModularVisualization import ModularServer
from evoagent.utils import *
from evoagent.SimpleContinuousModule import SimpleCanvas
import numpy as np
from evoagent.network_chart import PopChart

def run(seed=0):

    pop_diff = pickle.load(open(f'./data/difficult_envS{seed}/save_pop/step10000.pickle', 'rb'))
    pop_easy = pickle.load(open(f'./data/easy_envS{seed}/save_pop/step10000.pickle', 'rb'))
    pop_fluct = pickle.load(open(f'./data/fluctuating_envS{seed}/save_pop/step10000.pickle', 'rb'))

    min_pop = np.min([len(pop_diff), len(pop_easy), len(pop_fluct)])
    pop_diff = np.random.choice(pop_diff, min_pop, replace=False)
    pop_easy = np.random.choice(pop_easy, min_pop, replace=False)
    pop_fluct = np.random.choice(pop_fluct, min_pop, replace=False)

    all_pop = np.hstack([pop_easy, pop_diff, pop_fluct])

    size = (1000, 1000)

    name_run = f"difficult_easy_popS{seed}"

    evo_canvas = SimpleCanvas(*size, name_run)

    epochs = deque([Epoch(10000, [0.8]*100)])
    model_params = {
        "pop": all_pop,
        "epochs": epochs,
        "size": size,
        "name_run": name_run
    }


    pop_chart = PopChart([f'difficult_envS{seed}', f'easy_envS{seed}', f'fluctuating_envS{seed}'], render_with_canvas=False, plot_every=50)

    server = ModularServer(model_factory, [input_chart, output_chart, evo_canvas, pop_chart], "EvoAgent", model_params, verbose=False)
    server.launch()


if __name__ == '__main__':
    run()