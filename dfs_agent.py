import time
import random
from copy import deepcopy
from agent import Agent, Map

#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque


class DFSMap(Map):

    def targetTraverse(self, start_position, target_position, path: list(), visited_list: list()):
        path += self.DFS(start_position, target_position)
        return super().targetTraverse(start_position, target_position, path, visited_list)
    
    def DFS(self, initial_position : list(),  target_position : list()):

        """
        DFS implementation
        """
        # Clear is visited
        self.clearIsVisited()

        start_node = self.findNodeFromPositionRef(initial_position)
        stack = [start_node]
        stack_path = [[start_node]]
        
        while stack:
            node, path = stack.pop(), stack_path.pop()
            
            if not node.is_visited:
                if node.position == target_position:
                    return path
                node.is_visited = True
                for adj_node in node.adj:
                    stack.append(adj_node)
                    stack_path.append(path+[adj_node])
                    self.expanded_node_count += 1
            pass
    



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
        
        
        self.map_manager = DFSMap(initial_level_matrix)
        paths, move_sequence = self.map_manager.calculateToAllTarget()
        self.expanded_node_count = self.map_manager.expanded_node_count
        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence