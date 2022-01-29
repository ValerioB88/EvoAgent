from collections import namedtuple, deque
Epoch = namedtuple('Epoch', ['init_step', 'energy_list'])


def find_pop_idx_from_id(agents, id):
    for idx, a in enumerate(agents):
        if a.unique_id == id:
            break
    return idx