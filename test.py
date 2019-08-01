import gym                                           
import time                                          
import json                                          
import random
import time
env = gym.make('gym_tdw:tdw_puzzle_1-v0')            
env.set_observation(True)                            
for i in range(100):                                  
    action = {"x": random.randint(-15,15),"z": random.randint(-15,15) }                                                                                                                                                                                                                                                            
    t = time.time()
    obs, reward, episode_done, _ = env.step(action)  
    print(reward,time.time()-t)
env.close()
