import time
import random
from copy import deepcopy
from agent import Agent, Map
from models import BFSMap

#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque


class BFSMap(Map):

    def targetTraverse(self, start_position, target_position, path: list(), visited_list: list()):
        path += self.BFS(start_position, target_position)
        return super().targetTraverse(start_position, target_position, path, visited_list)
    
    def BFS(self, initial_position : list(),  target_position : list()):

        """
        BFS implementation
        """
        # Clear is visited
        self.clearIsVisited()

        queue = [[self.findNodeFromPositionRef(initial_position)]]
        
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node.is_visited == False:
                neighbours = node.adj
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    
    
                    if neighbour.position == target_position:
                        print("Path", *new_path)
                        return new_path
                node.is_visited = True
    
        return None



class BFSAgent(Agent):

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
        
        self.map_manager = BFSMap(initial_level_matrix)
        paths,move_sequence = self.map_manager.calculateToAllTarget()
        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence