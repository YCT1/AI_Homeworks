import numpy as np

from game import *


class CarGameDQN(CarGame):
    def __init__(self, render=True, human_player=False):
        super(CarGameDQN, self).__init__(render, human_player)
        
        """
        DEFINE YOUR OBSERVATION SPACE DIMENSIONS HERE FOR EACH MODE.
        JUST CHANGING THE "obs_space_dim" VARIABLE SHOULD BE ENOUGH
        
            Try making your returned state from get_state function
        a 1-D array if its not, it will make things simpler for you
        """
        obs_space_dim = 6*5
        self.observation_space = spaces.Box(0, obs_space_dim, shape=(obs_space_dim,))
        
       

    def get_state(self):
        """
        Define your state representation here
        
        self.game_state gives you original [6][5] game grid array
        """
        state = None
        
        
        #  fill here
        
        
        # since state is list we can transform it to torch object
        # I want to use direct state representation but I will flatten it
        state = self.game_state

        # First I will create 6*5 matrix
        state_matrix = np.zeros(shape=(6,5))

        for i, row in enumerate(state):
            for j, item in enumerate(row):
                if item == "e":
                    state_matrix[i][j] = 0
                elif item == "r":
                    state_matrix[i][j] = 5
                else:
                    state_matrix[i][j] = 1

        # Return flattened version size of 35
        return state_matrix.flatten()



    def get_reward(self):
        """
        Define your reward calculations here
        
        :return:
            A value between (-1, 1)
        """
        self.reward = None
        
        if self.IsCrashed():
            self.reward = -0.6
        else:
            self.reward = 0.2
        #  fill here


        self.total_reward += self.reward
        return self.reward



