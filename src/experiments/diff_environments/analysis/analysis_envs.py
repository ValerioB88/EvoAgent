import pathlib
import glob
import pandas as pd
import matplotlib.pyplot as plt
def get_data(run):
    data = f'./data/{run}/collectors/env_state/'
    all_files = glob.glob(data + '/**')

    df = pd.DataFrame([])
    for f in all_files:
        df = df.append(pd.read_csv(f))

    return df


def plot(env):
    df = get_data(env)
    plt.figure(1)
    plt.plot(df['step'], df['num_agents'], label=env)
    plt.legend()
    plt.title('Tot Num. Agents')

    plt.figure(2)
    plt.plot(df['step'], df['num_agents']/df['num_food'], label=env)
    plt.legend()
    plt.title('Num. Agents/Num. Food')
    plt.figure(3)

    plt.plot(df['step'], df['num_food'], label=env)
    plt.legend()

    ratio = df["num_agents"] / df["num_food"]
    print(f'Env: {env}: {ratio.mean()}, {ratio.std()}')

plt.close('all')
plot('difficult_envS0')
plot('easy_envS0')
plot('fluctuating_envS0')

folder = './docs/assets/experiments/diff_environments/'
pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
plt.figure(1)
plt.savefig(folder + 'num_agents.png', dpi=300)
plt.figure(2)
plt.savefig(folder + 'agents_over_food.png', dpi=300)
plt.figure(3)
plt.savefig(folder + 'num_food.png', dpi=300)