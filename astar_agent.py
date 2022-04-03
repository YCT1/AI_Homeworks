import time
import random
from copy import deepcopy
from agent import Agent, Map, Node
from models import AStart

#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque


"""
  you may use the following Node class
  modify it if needed, or create your own
"""
class AStart(Map):
    def createmap(self, map_matrix: list()):

        # Copy map matrix to walk matrix
        self.walk_matrix = deepcopy(map_matrix)
        self.walk_matrix = self.fill(self.walk_matrix, False)

        # Traverse though map
        for y, row in enumerate(map_matrix):
            for x, element in enumerate(row):
                if element == "F" or element == "B" or element == "T" or element == "S" or element == "D":
                    
                    # Create Node
                    node = Node(element,[x,y])

                    # Node add to the list
                    self.nodes.append(node)

                    # Set True value to at the walkable matrix
                    self.walk_matrix[y][x] = True
        
        # Create adj connection to each  node
        self.createAdjConnections()

    def targetTraverse(self, start_position, target_position, path: list(), visited_list: list()):
        
        # Call A* with manhattan algorithm
        path += self.aStartAlgorithm(start_position, target_position, self.h_manhattan)
        return super().targetTraverse(start_position, target_position, path, visited_list)
    
    def h_manhattan(self, start_position: list(), target_position: list()):
        """
        H function (Manhattan version)
        """
        dx = target_position[0] - start_position[0]
        dy = target_position[1] - start_position[1]
        return abs(dx) + abs(dy)

    def aStartAlgorithm(self, start_position: list(), target_position: list(), heuristic):
        # In this open_lst is a lisy of nodes which have been visited, but who's 
        # neighbours haven't all been always inspected, It starts off with the start 
        #node
        # And closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always inspected
        start = self.findNodeFromPositionRef(start_position)
        target = self.findNodeFromPositionRef(target_position)

        open_lst = set([start])
        closed_lst = set([])
 
        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo = {}
        poo[start] = 0
 
        # par contains an adjac mapping of all nodes
        par = {}
        par[start] = start
 
        while len(open_lst) > 0:
            n = None
 
            # it will find a node with the lowest value of f() -
            for v in open_lst:
                if n == None or poo[v] + heuristic(v.position,target_position) < poo[n] + heuristic(n.position, target_position):
                    n = v
 
            if n == None:
                print('Path does not exist!')
                return None
 
            # if the current node is the stop
            # then we start again from start
            if n == target:
                reconst_path = []
 
                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]
 
                reconst_path.append(start)
 
                reconst_path.reverse()
 
                print('Path found: {}'.format(reconst_path))
                return reconst_path
 
            # for all the neighbors of the current node do
            for adj_node in n.adj:
              # if the current node is not presentin both open_lst and closed_lst
                # add it to open_lst and note n as it's par
                if adj_node not in open_lst and adj_node not in closed_lst:
                    open_lst.add(adj_node)
                    par[adj_node] = n
                    poo[adj_node] = poo[n] + adj_node.cost
 
                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update par data and poo data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if poo[adj_node] > poo[n] + adj_node.cost:
                        poo[adj_node] = poo[n] + adj_node.cost
                        par[adj_node] = n
 
                        if adj_node in closed_lst:
                            closed_lst.remove(adj_node)
                            open_lst.add(adj_node)
 
            # remove n from the open_lst, and add it to closed_lst
            # because all of his neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)
 
        print('Path does not exist!')
        return None



class AStarAgent(Agent):

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
        initial_h = None  #  fill this value with your heuristic function

        
        self.map_manager = AStart(initial_level_matrix)
        _,move_sequence = self.map_manager.calculateToAllTarget()

        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence