from sos_environment.env import sos_environment

env = sos_environment.env(render_mode="cmdd")
env.reset(seed=42)

print(env.observation_space(env.agent_selection))
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()
    print(env.observation_space(agent))

    if termination or truncation:
        action = None
    else:

        # this is where you would insert your policy
        action = env.action_space(agent).sample()

    env.step(action)
    env.render()

env.close()