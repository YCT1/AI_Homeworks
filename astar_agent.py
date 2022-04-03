import time
import random
import math
from agent import Agent, Map


#  use whichever data structure you like, or create a custom one


class AStart(Map):
    def walkableCells(self, element: str) -> bool:
        """
        It check and return true if cell is desired walkable cells Overwritten for level2
        """
        return element == "F" or element == "B" or element == "T" or element == "S" or element == "D"  

    def targetTraverse(self, start_position, target_position, path: list(), visited_list: list()):
        
        # Call A* with manhattan algorithm
        path += self.aStartAlgorithm(start_position, target_position, self.h_manhattan)
        return super().targetTraverse(start_position, target_position, path, visited_list)
    
    def h_manhattan(self, start_position: list(), target_position: list()) -> int:
        """
        H function (Manhattan version)
        """
        dx = target_position[0] - start_position[0]
        dy = target_position[1] - start_position[1]
        return abs(dx) + abs(dy)

    def h_euclidean(self, start_position: list(), target_position: list()) -> float:
        """
        H function (Euclidean version)
        """
        dx = target_position[0] - start_position[0]
        dy = target_position[1] - start_position[1]
        return math.sqrt(dx**2 + dy**2)

    
    def aStartAlgorithm(self, start_position: list(), target_position: list(), heuristic):
       
        # Let's get node from their position respectively
        start = self.findNodeFromPositionRef(start_position)
        target = self.findNodeFromPositionRef(target_position)


        # We are going to use Python's set data structure, this data structure is exacatly what we need
        # We need and "open set", these will store visited nodes that can be expanded
        # We need to add start (root) to the our set
        open_set = set([start])
        self.expanded_node_count += 1 # For stats

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

            if len(open_set) + len(closed_set) >= self.maximum_node_in_memory_count:
                self.maximum_node_in_memory_count = len(open_set) + len(closed_set)
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
                    self.expanded_node_count += 1 # For stats
 
                
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
                            self.expanded_node_count += 1 # For stats
 
            # All adj nodes are explored thus it is closed case
            open_set.remove(n)
            closed_set.add(n)
            self.generated_node_count += 1 # For stats
 
        # If that point, we cannot find anything thus there is no any route
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

        # Get stats
        self.generated_node_count, self.expanded_node_count = self.map_manager.generated_node_count, self.map_manager.expanded_node_count
        self.expanded_node_count = self.map_manager.expanded_node_count
        self.maximum_node_in_memory_count = self.map_manager.maximum_node_in_memory_count

        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence