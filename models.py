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
       
        # Let's get node from their position respectively
        start = self.findNodeFromPositionRef(start_position)
        target = self.findNodeFromPositionRef(target_position)


        # We are going to use Python's set data structure, this data structure is exacatly what we need
        # We need and "open set", these will store visited nodes that can be expanded
        # We need to add start (root) to the our set
        open_set = set([start])

        # This set will store all expanded nodes and discovered nodes (nodes that all children nodes are explored)
        closed_set = set([])
 
        # In this part, We can use Python's dict to store cost from start to that found node
        cost_dict = {}
        cost_dict[start] = 0
 
        # Neughboards mapping of all node
        came_from = {}
        came_from[start] = start
 
        while open_set:
            n = None
 
            # Find lowest cost node  (Apply A* formula)
            for v in open_set:
                # N is empty fill it
                if n == None:
                    n = v
                if cost_dict[v] + heuristic(v.position,target_position) < cost_dict[n] + heuristic(n.position, target_position):
                     n = v

            # If n is still  none thus there is no route 
            if n == None:
                return None
 
            # If we reach the target, we need to re-constract the path using came_from dict
            if n == target:
                final_path = []
 
                while came_from[n] != n:
                    final_path.append(n)
                    n = came_from[n]
 
                final_path.append(start)
                final_path.reverse()
                print("Path", *final_path)
                return final_path
 
            # Traverse though adj of n
            for adj_node in n.adj:
                # If we not visited this node n at all,
                if (adj_node not in open_set) and (adj_node not in closed_set):
                    
                    # Store the path
                    came_from[adj_node] = n

                    # Store the cost
                    cost_dict[adj_node] = cost_dict[n] + adj_node.cost

                    # Add to the set of open_set
                    open_set.add(adj_node)
 
                
                else:
                    # However, if it is better deal to go in that route
                    if cost_dict[n] + adj_node.cost < cost_dict[adj_node]:
                        # Store path and cost
                        cost_dict[adj_node] = cost_dict[n] + adj_node.cost
                        came_from[adj_node] = n

                        # We need to remove if that adj_node in close set because we can explore more
                        if adj_node in closed_set:
                            closed_set.remove(adj_node)
                            open_set.add(adj_node)
 
            # All adj nodes are explored thus it is closed case
            open_set.remove(n)
            closed_set.add(n)
 
        # If that point, we cannot find anything thus there is no any route
        return None

    

m = AStart(map3)
_,p  =m.calculateToAllTarget()
print(p)

