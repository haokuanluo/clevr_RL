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
from PIL import Image
env = gym.make('gym_tdw:tdw_puzzle_1-v0')
env.set_observation(True)

for i in range(30):
    if i == 0 or i == 100:
        action = env.sample_random_action()
    else:
        action = {
            "x": 0,
            "z": 0
        }

    obs, reward, episode_done, _ = env.step(action)

# Wait until the simulator sends all messages
time.sleep(20)



```
## Puzzles
### Puzzle 1  
![Puzzle 1 image](https://github.ibm.com/Abhi-B/gym-tdw/blob/master/puzzle_images/puzzle_1.png)  
### Puzzle 2  
![Puzzle 2 image](https://github.ibm.com/Abhi-B/gym-tdw/blob/master/puzzle_images/puzzle_2.png)  
### Puzzle 3  
![Puzzle 3 image](https://github.ibm.com/Abhi-B/gym-tdw/blob/master/puzzle_images/puzzle_3.png)  
### Puzzle 4  
![Puzzle 4 image](https://github.ibm.com/Abhi-B/gym-tdw/blob/master/puzzle_images/puzzle_4.png)  
### Puzzle 5  
![Puzzle 5 image](https://github.ibm.com/Abhi-B/gym-tdw/blob/master/puzzle_images/puzzle_5.png)  
### Puzzle 6  
![Puzzle 6 image](https://github.ibm.com/Abhi-B/gym-tdw/blob/master/puzzle_images/puzzle_6.png)  
### Puzzle 7  
![Puzzle 7 image](https://github.ibm.com/Abhi-B/gym-tdw/blob/master/puzzle_images/puzzle_7.png)  
