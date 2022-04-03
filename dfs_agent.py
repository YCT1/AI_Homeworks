import time
import random
from copy import deepcopy
from agent import Agent
from models import DFSMap

#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque






class DFSAgent(Agent):

    def __init__(self):
        super().__init__()

    def solve(self, level_matrix, player_row, player_column):
        super().solve(level_matrix, player_row, player_column)
        move_sequence = []

        """
            YOUR CODE STARTS HERE
            fill move_sequence list with directions chars
        """

        initial_level_matrix = [list(row) for row in level_matrix] #deepcopy(level_matrix)
        
        
        myMap = DFSMap(initial_level_matrix)
        paths, move_sequence = myMap.calculateToAllTarget()
        
        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence