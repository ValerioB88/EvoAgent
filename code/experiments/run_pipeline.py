from experiments import difficult_env, easy_env

difficult_env.run(0)
difficult_env.run(1)

[difficult_env.run(s) for s in range(10)]
[easy_env.run(s) for s in range(10)]