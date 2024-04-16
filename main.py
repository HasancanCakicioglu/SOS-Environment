from sos_environment.env import sos_environment

env = sos_environment.env(render_mode="cmd")
env.reset(seed=42)

print(env.observation_space(env.agent_selection))
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
    else:
        mask = observation["action_mask"]
        print(mask)
        print("by")
        print(env.apply_mask(mask))
        # this is where you would insert your policy
        action = env.action_space(agent).sample(env.apply_mask(mask))

    env.step(action)
env.close()