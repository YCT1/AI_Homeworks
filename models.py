import copy
from ctypes import Union
from importlib.resources import path
from typing import Tuple



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
        pass
    
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
        This function need to be overriden in the child classes
        """
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
    def __init__(self, map_matrix: list()) -> None:
        super().__init__(map_matrix)
    
    def targetTraverse(self, start_position, target_position, path: list(), visited_list: list()):
        path += self.BFS(start_position, target_position)
        
        # Get targets
        targets = self.findNodeFromTypeRef("T")

        for target in targets:
            if target not in visited_list:
                visited_list.append(target)
                self.targetTraverse(target_position, target.position, path,visited_list )
        
        return path
    
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
    def __init__(self, map_matrix: list()) -> None:
        super().__init__(map_matrix)
    
    def targetTraverse(self, start_position, target_position, path: list(), visited_list: list()):
        path += self.DFS(start_position, target_position)
        
        # Get targets
        targets = self.findNodeFromTypeRef("T")

        for target in targets:
            if target not in visited_list:
                visited_list.append(target)
                self.targetTraverse(target_position, target.position, path,visited_list )
        
        return path
    
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
    
  

