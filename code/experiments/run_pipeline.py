from experiments import difficult_env, easy_env, fluctuating_env, easy_difficult_pops


# [difficult_env.run(s) for s in range(9, 10)]
[easy_env.run(s) for s in range(10)]
[fluctuating_env.run(s) for s in range(10)]

[easy_difficult_pops.run(s) for s in range(10)]