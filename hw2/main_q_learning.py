from collections import namedtuple
import time

import numpy as np


from game_q_learning import CarGameQL
from macros import *
import random

# Are we rendering or not
RENDER_TRAIN = False


"""
    Parameters related to training process and Q-Learning
"""

# Number of episodes to train
NUM_EPISODES = 1000

# epsilon parameter of e-greedy policy
EPSILON = 0.1

# learning rate parameter of q learning
LEARNING_RATE = 0.3

# discount rate parameter of q learning
DISCOUNT_RATE = 0.9

# The step limit per episode, since we do not want infinite loops inside episodes
MAX_STEPS_PER_EPISODE = 200

"""
    Parameters end
"""



# Here, we are creating the environment with our predefined observation space
env = CarGameQL(render=RENDER_TRAIN)

# Observation and action space
obs_space = env.observation_space
number_of_states = env.observation_space.shape[0]

action_space = env.action_space
number_of_actions = env.action_space.n
print("The observation space: {}".format(obs_space))
# Output: The observation space: Box(n,)
print("The action space: {}".format(action_space))
# Output: The action space: Discrete(m)



# I decided to implement Q table as
# {
#   ...    
#   state_n : [q_value_right, q_value_left, q_value_stay]
#   ...
# }
# Note that: right:0,  left:1, stay:2
q_table = {}


def choose_action_greedy(state, q_table):
    action = None
    # Firstly let's check if our state in the q_table
    if not state in q_table:
        # It is not in the list
        
        # Let's inilizate it with zero values
        q_table[state] = [0,0,0]

        # Chose random action
        action = random.randint(0,2)
        return action
    else:
        # so our action in the list
        # Find maximum of the action and return it
        q_values_of_this_state = q_table[state]
        
        # This is first implementation
        # Since list.index() call returns first occurence
        # It is biased towards to 0 action "right"
        #action = q_values_of_this_state.index(max(q_values_of_this_state))

        # This is very interensting approach, I tried to force car to stay more offeten
        # If we have equal number of Q values and one of them is stay chose stay
        # Othervise randomly select
        indices = [index for index, item in enumerate(q_values_of_this_state) if item == max(q_values_of_this_state)]
        if len(indices) < 2:
            action = indices[0]
            return action
        if 2 in indices:
            # Chose stay if retured max q values consist stay
            action = 2
            return action
        action = indices[random.randint(0, len(indices)-1)]
        return action


def choose_action_e_greedy(state, q_table):
    action = None
    if not state in q_table:
        # It is not in the list
        
        # Let's inilizate it with zero values
        q_table[state] = [0,0,0]

        # Chose random action
        action = random.randint(0,2)
        return action
    else:
        # If state is in table
        # chose with epsilon gredy approach

        p = random.random()

        if p <= EPSILON:
            # Chose random action
            action = random.randint(0,2)
            return action
        else:
            # Select best action
            q_values_of_this_state = q_table[state]
        
            indices = [index for index, item in enumerate(q_values_of_this_state) if item == max(q_values_of_this_state)]
            if len(indices) < 2:
                action = indices[0]
                return action
            if 2 in indices:
                # Chose stay if retured eqaul max q values consist stay
                action = 2
                return action
            action = indices[random.randint(0, len(indices)-1)]
            return action



def main():
    #  "Loop for each episode:"
    for e in range(NUM_EPISODES):
        #  "Initialize S"
        s0 = env.reset()

        #  "Loop for each step of episode:"
        episode_steps = 0
        while (episode_steps < MAX_STEPS_PER_EPISODE):
            #
            #  "Choose A from S using policy derived from Q (e.g., e-greedy)"
            #

            # Chose action from current state by locking q table
            action = choose_action_e_greedy(s0, q_table)

            #  "Take action A, observe R, S'"
            s1, reward, done, info = env.step(action)
            
            
            #
            #  "Q(S,A) <-- Q(S,A) + alpha*[R + gamma* maxa(Q(S', a)) - Q(S, A)]"
            #

            # Next step check
            if not s1 in q_table:
                q_table[s1] = [0,0,0]
            
            q_table[s0][action] = q_table[s0][action] + LEARNING_RATE* (reward  + DISCOUNT_RATE* max(q_table[s1]) - q_table[s0][action])
            #  "S <-- S'"
            s0 = s1
            
            #until S is terminal
            if (done):
                break
            
            episode_steps += 1
        #  print number of episodes so far
        if (e %100 == 0):
            print("episode {} completed".format(e))
    
    
    
    
    #  test our trained agent
    test_agent(q_table)



def test_agent(q_table):
    print("Initializing test environment:")
    test_env = CarGameQL(render=True, human_player=False)
    state = env.reset()
    steps = 0
    #while (steps < 200):
    while (True):
        action = choose_action_greedy(state, q_table)
        print("chosen action:", action)
         
        # Modified
        #next_state, reward, done, info = test_env.step(convert_direction_to_action(action))
        next_state, reward, done, info = test_env.step(action)
        print("state:", state, " , next_state:", next_state)
        test_env.render()
        if done:
            break
        else:
            state = next_state
        steps += 1
        print("test current step:",steps)
        
        time.sleep(0.1)


if __name__ == '__main__':
    main()


