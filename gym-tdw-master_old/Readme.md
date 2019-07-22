# Openai gym for tdw

Install the gym environment
```
git clone git@github.ibm.com:Abhi-B/gym-tdw.git && cd gym-tdw

pip install -e .
```
* Copy the gym-tdw/envs/TDW folder in same folder as your code  
* Download TDW release from the github repository  
## To Run:
* Write your code to use gym or copy the below example code  
* Makesure the TDW folder is in same folder
* Run the TDW/db_server.py and TDW/server.py
* Now run the code  
## Example usage
```
import gym
import time
env = gym.make('gym_tdw:tdw-v0')
env.set_observation(True)

for i in range(200):
    if i == 0 or i == 100:
        action = env.sample_random_action()

    else:
        action = {
            "x": 0,
            "z": 0
        }

    obs, reward, episode_done, _ = env.step(action)

    if episode_done:
        break

# Wait until the simulator sends all messages
time.sleep(20)

```
