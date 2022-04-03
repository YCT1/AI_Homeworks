import copy
from ctypes import Union
from typing import Tuple
from math import sqrt




map1 =  [['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'T', 'F', 'F', 'T', 'F', 'F', 'F', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'B', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]
 
map2 = [['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
 ['W', 'F', 'F', 'T', 'F', 'F', 'F', 'W', 'W', 'W', 'W', 'W', 'W'],
 ['W', 'F', 'W', 'W', 'W', 'W', 'F', 'W', 'W', 'W', 'W', 'W', 'W'],
 ['W', 'T', 'F', 'F', 'F', 'B', 'F', 'T', 'F', 'F', 'F', 'T', 'W'],
 ['W', 'W', 'W', 'W', 'F', 'W', 'F', 'W', 'W', 'W', 'W', 'W', 'W'],
 ['W', 'W', 'W', 'W', 'F', 'F', 'F', 'W', 'W', 'W', 'W', 'W', 'W'], 
 ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]


map3 =  [['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
 ['W', 'W', 'W', 'W', 'W', 'W', 'F', 'F', 'F', 'F', 'F', 'W'],
 ['W', 'W', 'W', 'W', 'W', 'W', 'F', 'W', 'W', 'W', 'F', 'W'],
 ['W', 'W', 'W', 'W', 'W', 'W', 'F', 'W', 'W', 'W', 'F', 'W'], 
 ['W', 'W', 'W', 'W', 'W', 'W', 'F', 'W', 'W', 'W', 'F', 'W'],
 ['W', 'W', 'W', 'W', 'W', 'W', 'F', 'S', 'S', 'S', 'F', 'W'],
 ['W', 'F', 'T', 'F', 'F', 'B', 'F', 'W', 'W', 'W', 'T', 'W'],
 ['W', 'W', 'W', 'W', 'W', 'W', 'F', 'D', 'D', 'F', 'F', 'W'],
 ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]

class Node:
    def __init__(self, type : str, position : list()) -> None:

        # Type of Node
        self.type = type

        # Position of the node
        self.position = position

        # Adjecent nodes
        self.adj = list()

        # KeyList to adj nodes 
        self.keys = list()

        # is Visited Mark
        self.is_visited = False

        # Cost (For AStart Algorithm)
        self.cost = self.getCostByType(type)
        pass
    
    def getCostByType(self, type: str) -> int:
        type_cost = {
        "F": 1,
        "S": 2,
        "D": 4,
        "T" : 1,
        "B" : 1
        }
        return type_cost[type]

    def __str__(self) -> str:
        return f"{self.position}"


class Map:
    def __init__(self, map_matrix: list()) -> None:
        
        self.nodes = list()
        # It is walkable matrix True are walkable, False are not walkable
        self.walk_matrix = list()

        # Create a map
        self.createmap(map_matrix)

        # Baby Position
        self.baby_position = self.nodes[self.findNodeFromType("B")].position


    def fill(self, matrix : list(), value) -> list():

        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                matrix[y][x] = value
        return matrix

    def findNodeFromPosition(self, position: list()) -> int:
        """
        This function search nodes from the list if it could not find return -1
        """

        for idx, node in enumerate(self.nodes):
            if node.position == position:
                return idx
        return -1
    
    def findNodeFromType(self, type: str) -> list():
        """
        Finds nodes from its type returns indexes of list
        """
        results = list()
        for idx, node in enumerate(self.nodes):
            if node.type == type:
                results.append(idx)
        
        if len(results) == 1:
            return results[0]
        else:
            return results

    
    def findNodeFromTypeRef(self, type: str) -> list():
        """
        Find nodes from its type returns a list of references
        """
        results = list()
        for idx, node in enumerate(self.nodes):
            if node.type == type:
                results.append(node)
        
        if len(results) == 1:
            return results[0]
        else:
            return results
    
    def createAdjConnections(self):
        for i in range(len(self.nodes)):
            x,y = self.nodes[i].position[0], self.nodes[i].position[1]
            
            # Up Side
            up_node = self.findNodeFromPosition([x,y+1])
            if up_node != -1:
                self.nodes[i].adj.append(self.nodes[up_node])
                self.nodes[i].keys.append("D")
            
            # Down Side
            down_node = self.findNodeFromPosition([x,y-1])
            if down_node != -1:
                self.nodes[i].adj.append(self.nodes[down_node])
                self.nodes[i].keys.append("U")

            # Left Side
            left_node = self.findNodeFromPosition([x-1,y])
            if left_node != -1:
                self.nodes[i].adj.append(self.nodes[left_node])
                self.nodes[i].keys.append("L")

            # Right Side
            right_node = self.findNodeFromPosition([x+1,y])
            if right_node != -1:
                self.nodes[i].adj.append(self.nodes[right_node])
                self.nodes[i].keys.append("R")
            
    def createmap(self, map_matrix: list()):

        # Copy map matrix to walk matrix
        self.walk_matrix = copy.deepcopy(map_matrix)
        self.walk_matrix = self.fill(self.walk_matrix, False)

        # Traverse though map
        for y, row in enumerate(map_matrix):
            for x, element in enumerate(row):
                if element == "F" or element == "B" or element == "T":
                    
                    # Create Node
                    node = Node(element,[x,y])

                    # Node add to the list
                    self.nodes.append(node)

                    # Set True value to at the walkable matrix
                    self.walk_matrix[y][x] = True
        
        # Create adj connection to each  node
        self.createAdjConnections()
    
    def setNodeVisited(self, position: list(), value = True):
        self.nodes[self.findNodeFromPosition(position)].is_visited = value

    
    def findNodeFromPositionRef(self, position: list()) -> Node:
        """
        This function search nodes from the list if it could not find return -1
        """
        for idx, node in enumerate(self.nodes):
            if node.position == position:
                return node
        return None


    def clearIsVisited(self, value = False) -> None:
        """
        Clears is_visited flag on all nodes
        """
        for node in self.nodes:
            node.is_visited = value


    

    def calculateRoute(self, path: list()) -> list:
        """
        This function gets path as list of Node and transforms it to key presses
        """
        keys = list()

        for idx, node in enumerate(path):
            if idx != len(path)-1:
                next_node = path[idx+1]
                if next_node != node:
                    index_next = node.adj.index(next_node)
                    keys.append(node.keys[index_next])

        return keys

    def targetTraverse(self, start_position, target_position, path:list(), visited_list: list()):
        """
        This function need modify in the child classes
        """

        # Get targets
        targets = self.findNodeFromTypeRef("T")

        for target in targets:
            if target not in visited_list:
                visited_list.append(target)
                self.targetTraverse(target_position, target.position, path,visited_list )
        
        return path
        pass
    
    def calculateToAllTarget(self) -> Tuple[list, list]:
        """
        This functions brute forcely calculates all posible travel of on all target,
        Returns all posible paths and shortest path with keys values
        """
        start_position = self.baby_position
        target_locations = self.findNodeFromTypeRef("T")
        print( "Targets: ",*target_locations)
        
        paths = list()
        for target in target_locations:
            p = self.targetTraverse(start_position, target.position, list(), [target])
            paths.append(p)
            pass
        
        key_paths = list()
        for path in paths:
            key_paths.append(self.calculateRoute(path))
        
        
        shortest_path_keys = min(key_paths,key=len)
        return paths,shortest_path_keys
       
        




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
            pass
    
  

class AStart(Map):
    def createmap(self, map_matrix: list()):

        # Copy map matrix to walk matrix
        self.walk_matrix = copy.deepcopy(map_matrix)
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

    def h_euclidean(self, start_position: list(), target_position: list()):
        """
        H function (Euclidean version)
        """
        dx = target_position[0] - start_position[0]
        dy = target_position[1] - start_position[1]
        r = sqrt(dx**2 + dy**2)
        print("AA", r)
        return r
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

