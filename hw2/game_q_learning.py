from matplotlib.pyplot import step
import numpy as np

from game import *


class CarGameQL(CarGame):
    def __init__(self, render=True, human_player=False):
        super(CarGameQL, self).__init__(render, human_player)
        
        """
        DEFINE YOUR OBSERVATION SPACE DIMENSIONS HERE FOR EACH MODE.
        JUST CHANGING THE "obs_space_dim" VARIABLE SHOULD BE ENOUGH
        
            Try making your returned state from get_state function
        a 1-D array if its not, it will make things simpler for you
        
            For the first Q-Learning part, you must use a more compact
        game state than raw game array
        """
        obs_space_dim = 6
        self.observation_space = spaces.Box(0, obs_space_dim, shape=(obs_space_dim,))
        
       

    def get_state(self):
        """
        Define your state representation here
        
        self.game_state gives you original [6][5] game grid array
        """

        # Note that since we do not have multiple car in the same row, we can give identations
        # If row has
        #   0: Car is on left
        #   2: Car is on middle
        #   4: Car is on right
        #   -: There is no car at that row
        state = None
        
        
        #  fill here
        state = self.game_state
        
        new_state = list()
        for row in state:
            finded_position = "-"
            for i in range(len(row)):
                if row[i] == "b" or row[i] == "r":
                    finded_position = str(i)
                    break
            
            new_state.append(finded_position)

        # make string for dict format
        new_state_string = ' '.join([str(elem) for elem in new_state])
        return new_state_string
        

    def get_reward(self):
        """
        Define your reward calculations here
        """
        self.reward = None
        
        
        #  fill here

        if self.IsCrashed():
            self.reward = -5
        else:
            self.reward = 1
        
        self.total_reward += self.reward
        return self.reward



