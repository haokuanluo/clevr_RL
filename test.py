import gym
import time
import pickle

env = gym.make('gym_tdw:tdw_puzzle_1-v0')
env.set_observation(True)
print(env.action_space)
ar = []
for i in range(100):
    action = env.sample_random_action()
#    action = {'x':0,'z':0}
   # else:
   #     action = {
   #         "x": 0,
   #         "z": 0
   #     }

    obs, reward, episode_done, _ = env.step(action)
    print(reward)
    print(action)
    print(obs['image_1'].shape)
    ar.append(obs['image_1'])
    pickle.dump(ar,open('img.p','wb'))
    if episode_done:
        break

# Wait until the simulator sends all messages
time.sleep(20)
