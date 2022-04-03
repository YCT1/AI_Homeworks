import time
import copy
from ctypes import Union
from typing import Tuple
from xmlrpc.client import Boolean

# General Node Class 
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
        "T": 1,
        "B": 1
        }
        return type_cost[type]

    def __str__(self) -> str:
        return f"{self.position}"


class Agent:

    """
        initialize some member variables
    """
    def __init__(self):
        self.player_row = 0
        self.player_col = 0
        self.level_matrix = None
        self.elapsed_solve_time = 0

        """
            please use these variables for statistics
        """
        self.expanded_node_count = 0
        self.generated_node_count = 0
        self.maximum_node_in_memory_count = 0

        #  not implemented, not necessary
        self.real_distance_matrix = []
        self.manhattan_distance_matrix = []

        # Solver and Map Manager
        self.map_manager = None
    


    """
        returns REAL manhattan distance between two points in the level.
    it is the amount of steps required from going point 1 to point 2, 
    so it also consider walls.
    row_1 and col_1 is the position of first point
    row_2 and col_2 is the position of second point 

        this function is not necessary, you may leave it empty
    """
    def real_distance(self, row_1, col_1, row_2, col_2):
        raise NotImplementedError
    


    """
        level_matrix is list of lists (like 2d array)
    that contains whether a particular cell is
    -T (toy)
    -F (floor)
    -P (player)
    -W (wall)

    level_matrix[0][0] is top left corner
    level_matrix[height-1][0] is bottom left corner
    level_matrix[height-1][width-1] is bottom right corner

        player_row and player_column are current position
    of the player, eg:
    level_matrix[player_row][player_column] supposed to be P
      
        returns a character list, list of moves
    that needs to be played in order to solve
    given level
    valid letters are R, U, L, D corresponds to:
    Right, Up, Left, Down
    an example return value:
    L = ["U", "U", "U", "L", "R", "R"]...
    """
    def solve(self, level_matrix, player_row, player_column):
        self.player_row = player_row
        self.player_col = player_column
        self.level_matrix = level_matrix

        #  you may precompute distances between pairs of points here


# Map agent inherited from Agent Class
class Map(Agent):
    def __init__(self, map_matrix: list()) -> None:
        
        self.nodes = list()
        # It is walkable matrix True are walkable, False are not walkable
        self.walk_matrix = list()

        # Create a map
        self.createmap(map_matrix)

        # Baby Position
        self.baby_position = self.nodes[self.findNodeFromType("B")].position
        super().__init__()


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
        """
        For each node, and for each node's 4 side (up, down, right and left) firstly check if adjecent node exsist if exsist it adds to node's connections
        """
        for i in range(len(self.nodes)):
            x,y = self.nodes[i].position[0], self.nodes[i].position[1]

            # Down Side
            down_node = self.findNodeFromPosition([x,y+1])
            if down_node != -1:
                self.nodes[i].adj.append(self.nodes[down_node])
                self.nodes[i].keys.append("D")

            # Up Side
            up_node = self.findNodeFromPosition([x,y-1])
            if up_node != -1:
                self.nodes[i].adj.append(self.nodes[up_node])
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

    def walkableCells(self, element: str) -> bool:
        """
        It check and return true if cell is desired walkable cells, it can be overwritten for other maps
        """
        return element == "F" or element == "B" or element == "T"     
    
    def createmap(self, map_matrix: list()):
        """
        This function reads from the list and construct a map from using node objects
        """
        # Copy map matrix to walk matrix
        self.walk_matrix = copy.deepcopy(map_matrix)
        self.walk_matrix = self.fill(self.walk_matrix, False)

        # Traverse though map
        for y, row in enumerate(map_matrix):
            for x, element in enumerate(row):
                if self.walkableCells(element):
                    
                    # Create Node
                    node = Node(element,[x,y])

                    # Node add to the list
                    self.nodes.append(node)

                    # Set True value to at the walkable matrix
                    self.walk_matrix[y][x] = True
        
        # Create adj connection to each  node
        self.createAdjConnections()
    
    def setNodeVisited(self, position: list(), value = True):
        """
        Set a node visited or not by its position
        """
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
        This function need to be modified in the child classes
        """

        # Get targets
        targets = self.findNodeFromTypeRef("T")

        for target in targets:
            if target not in visited_list:
                visited_list.append(target)
                self.targetTraverse(target_position, target.position, path,visited_list )
        
        return path

    
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