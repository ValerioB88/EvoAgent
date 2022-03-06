from src.experiments.diff_environments import difficult_env, easy_env, fluctuating_env, multi_pops_test

seeds = 10
## Train 3 populations
[difficult_env.run(s) for s in range(seeds)]
[easy_env.run(s) for s in range(seeds)]
[fluctuating_env.run(s) for s in range(seeds)]

## Put them together
[multi_pops_test.run(s) for s in range(seeds)]






