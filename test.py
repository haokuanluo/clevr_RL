import gym
import time

env = gym.make('gym_tdw:tdw-v0')
env.set_observation(True)

for i in range(1):
    if i == 0 or i == 100:
        action = env.sample_random_action()

    else:
        action = {
            "x": 0,
            "z": 0
        }

    obs, reward, episode_done, _ = env.step(action)
    print(reward)
    print(obs)
    if episode_done:
        break

# Wait until the simulator sends all messages
time.sleep(20)
