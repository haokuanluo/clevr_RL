import gym                                           
import time                                          
import json                                          
env = gym.make('gym_tdw:tdw_puzzle_1-v0')            
env.set_observation(True)                            
for i in range(10):                                  
    if i == 0 or i == 35:                            
        action = {                                   
            "x": 70,                                 
            "z": -50                                 
            }                                            
    else:                                            
        action = {                                   
            "x": 0,                                  
            "z": 0                                   
            }                                                                                                                                                                                                                                                            
    obs, reward, episode_done, _ = env.step(action)  
    if i == 10:                                      
        env.reset()                                  
env.close()
