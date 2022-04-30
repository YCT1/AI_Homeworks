import time
import sys
import os
from copy import deepcopy


import pygame

#  import game object classes
from level import Level
from player import Player
from apple import Apple
from toy import Toy

#  import constant definitions
from macros import *


#  import agents
from agent import Agent



class Game:
    def __init__(self, game_window_name="Hamham"):
        #  initialize pygame stuff
        pygame.display.init()
        pygame.mixer.init()
        pygame.display.set_caption(game_window_name)
        self.screen = pygame.display.set_mode(game_window_size)
        self.clock = pygame.time.Clock()
        
        #wall_width = self.wall.get_width()
        wall_width = 36

		# Load images
        self.wall = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/wall.png').convert(), (wall_width, wall_width))
        
        self.apple = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/apple_bg.png').convert(), (wall_width, wall_width))
        self.floor = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/floor.png').convert(), (wall_width, wall_width))
        self.grass = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/grass.png').convert(), (wall_width, wall_width))

        #  images for 2021_2022_spring_ai_undergrad
        self.baby_2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/baby_2_bg.png').convert(), (wall_width, wall_width))
        self.baby_2_images = [self.baby_2, self.baby_2, self.baby_2, self.baby_2]
        self.sand = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/sand.png').convert(), (wall_width, wall_width))
        self.water = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/water_tile.png').convert(), (wall_width, wall_width))
        self.toy_1 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/toy_1_bg.png').convert(), (wall_width, wall_width))
        
        
        self.player_right = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/pacman_bg.png').convert(), (wall_width, wall_width))
        self.player_up = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/pacman_bg.png').convert(), (wall_width, wall_width)), 90.0)
        self.player_left = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/pacman_bg.png').convert(), (wall_width, wall_width)), True, False)
        self.player_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/images/pacman_bg.png').convert(), (wall_width, wall_width)), -90.0)
        self.player_image = self.player_right
        self.player_images = [self.player_right, self.player_up, self.player_left, self.player_down]

        #  load sounds
        self.win_sound = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '/sounds/tada.wav')
        self.lose_sound = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '/sounds/fail_trombone_4s.wav')

		# Dictionary to map images to characters in level matrix
        self.images = {'W': self.wall, 
                    'A': self.apple, 
                    'F': self.floor, 
                    'G': self.grass, 
                    'P': self.player_image,
                    'B': self.baby_2,
                    'S': self.sand,
                    'D': self.water,
                    'T': self.toy_1}

        self.cost_dict = {'A': 1, 
                    'F': 1, 
                    'G': 1, 
                    'P': 1,
                    'B': 1,
                    'S': 2,
                    'D': 4,
                    'T': 1}

        self.current_level = None
        self.current_level_number = 0

		#  player object
        self.player = None


        self.game_finished = False
        self.player_alive = True

        self.initial_level_matrix = None

        """
        Current level statistics
        """
        #  number of toys player collected so far in curret level
        self.collected_toy_count = 0

        #  number of all toys in the initial level configuration
        self.total_toy_count = 0

        #  number of time steps elapsed in a level
        self.elapsed_time_step = 0

        #  path cost
        self.path_cost_so_far = 0


    def draw_level(self, level_matrix):
        # Get image size to print on screen
        box_size = self.wall.get_width()

        # Print images for matrix
        for i in range(0, len(level_matrix)):
            for c in range(0, len(level_matrix[i])):
                self.screen.blit(self.images[level_matrix[i][c]], (c * box_size, i * box_size))
        pygame.display.update()


    def draw_level_search(self, level_matrix, dir):
        # Get image size to print on screen
        box_size = self.wall.get_width()

        if (dir != "X"):
            drs = ["R", "U", "L", "D"]
            self.images["B"] = self.baby_2_images[drs.index(dir)]

        # Print images for matrix
        for i in range(0, len(level_matrix)):
            for c in range(0, len(level_matrix[i])):
                self.screen.blit(self.images[level_matrix[i][c]], (c * box_size, i * box_size))
        pygame.display.update()


    def init_level(self, level):
        self.current_level = Level(level)
        #self.draw_level(self.current_level.get_matrix())

        #  mark game as not finished
        self.game_finished = False
        self.player_alive = True

        #  number of time steps elapsed in a level
        self.elapsed_time_step = 0

        #  path cost
        self.path_cost_so_far = 0

        #  initialize number of toys player collected so far in curret level
        self.collected_toy_count = 0
		

        #  create player object
        player_pos = self.current_level.get_baby_pos()
        player_current_row = player_pos[0]
        player_current_col = player_pos[1]
        self.player = Player(player_current_row, player_current_col)

        #  create toys
        self.toys = []
        toy_positions = self.current_level.get_toy_positions()
        for pos in toy_positions:
            r = pos[0]
            c = pos[1]
            self.toys.append(Toy(r, c))
        
        #  count number of toys
        self.total_toy_count = len(self.toys)
        #print("Number of toys in the level ", self.total_toy_count)

        self.initial_level_matrix = deepcopy(self.current_level.get_matrix())

    

    """
    Calculates distance between player and the closest toy to player
    """
    def get_closest_toy_to_player(self):
        player_pos = self.player.get_pos()
        pr = player_pos[0]
        pc = player_pos[1]

        minDist = 1000
        closestToy = None
        for toy in self.toys:
            toy_pos = toy.get_pos()
            rr = toy_pos[0]
            rc = toy_pos[1]
            dist = abs(pr - rr) + abs(pc - rc)
            if (dist < minDist):
                minDist = dist
                closestToy = toy
        
        return (closestToy, minDist)


    def step(self, player_direction, render=True):
        matrix = self.current_level.get_matrix()
        self.current_level.save_history(matrix)

        #Print toys
        #print(self.current_level.get_toy_positions())


		#  save old position of the player
        player_current_pos = self.player.get_pos()
        player_current_row = player_current_pos[0]
        player_current_col = player_current_pos[1]



		#  calculate new position of the player
        player_next_pos = self.player.move(player_direction)
        player_next_row = player_next_pos[0]
        player_next_col = player_next_pos[1]


        
        #  resolve static collisions for player
        next_cell = matrix[player_next_row][player_next_col]
        if (next_cell == "F"):
            #  next cell is floor
            pass
        elif (next_cell == "W"):
            #  next cell is wall
            #player cant pass here
            self.player.current_pos = self.player.prev_pos
        elif (next_cell == "G"):
            #  next cell is grass
            #player removes grass
            matrix[player_next_row][player_next_col] = "B"
        elif (next_cell == 'A'):
            #  next cell is apple
            #player removes apple
            matrix[player_next_row][player_next_col] = "B"
        elif (next_cell == 'T'):
            #  next cell is toy
            #baby removes toy
            matrix[player_next_row][player_next_col] = "B"
        elif (next_cell == "R"):
            #  next square is robot
            #will resolve later
            pass
        
        #  check if player collected an toy
        #  TO DO: create a 2d toy grid for faster check
        new_toys = []
        for toy in self.toys:
            toy_pos = toy.get_pos()
            toy_row = toy_pos[0]
            toy_col = toy_pos[1]
            if (player_next_row == toy_row and player_next_col == toy_col):
                #player removes toy
                #  check if game is finished
                self.collected_toy_count += 1
                if (self.collected_toy_count == self.total_toy_count):
                    self.game_finished = True
            else:
                new_toys.append(toy)
        self.toys = new_toys

            
        #  update game matrix
        level_matrix = self.current_level.get_matrix()
      
        player_prev_row = self.player.get_prev_row()
        player_prev_col = self.player.get_prev_col()
        player_next_row = self.player.get_row()
        player_next_col = self.player.get_col()


        #  prev tile in initial level matrix
        original_tile = self.initial_level_matrix[player_prev_row][player_prev_col]
        #print("Original tile:",original_tile)
        if (original_tile == "S"):
            level_matrix[player_prev_row][player_prev_col] = "S"
        elif (original_tile == "D"):
            level_matrix[player_prev_row][player_prev_col] = "D"
        else:  #(original_tile == "F"):
            level_matrix[player_prev_row][player_prev_col] = "F"
        
        
        #  next tile in initial level matrix
        next_tile = self.initial_level_matrix[player_next_row][player_next_col]
        self.path_cost_so_far += self.cost_dict[next_tile]

        level_matrix[player_next_row][player_next_col] = "B"
        #  draw
        if (render):
            self.images["B"] = self.baby_2_images[self.player.current_facing_index]
            self.draw_level(matrix)


        self.elapsed_time_step += 1

        #remaining_toy_count = len(self.current_level.get_toy_positions())
        #print("Number of remaining toys: ", remaining_toy_count)

        #  check if game is finished
        if (self.game_finished):
            if (self.player_alive):
                #  player collected all toys
                #print("Level completed!")
                return RESULT_PLAYER_WON
            else:
                #  player is dead
                #print("Player is killed by the robot!")
                return RESULT_PLAYER_DEAD
        else:
            return RESULT_GAME_CONTINUE


    #  function when a human player plays the game
    def start_level_human(self, level_index):
        self.init_level(level_index)
        self.draw_level(self.current_level.get_matrix())


		#  number of all toys in the initial level configuration
        self.total_toy_count = len(self.toys)
        

        self.distance_to_closest_toy = self.get_closest_toy_to_player()[1]

        #  game loop
        while True:
            result = 0

            #  manual input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #self.craft_features()

                    if event.key == pygame.K_RIGHT:
                        result = self.step("R", render=True)
                    elif event.key == pygame.K_UP:
                        result = self.step("U", render=True)
                    elif event.key == pygame.K_LEFT:
                        result = self.step("L", render=True)
                    elif event.key == pygame.K_DOWN:
                        result = self.step("D", render=True)
                    elif event.key == pygame.K_SPACE:
                        result = self.step("PASS", render=True)
                    #elif event.key == pygame.K_u:
                    #    self.draw_level(self.current_level.undo())
                    elif event.key == pygame.K_r:
                        self.init_level(self.current_level_number)
                        result = RESULT_GAME_CONTINUE
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    
                    
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if (result == RESULT_PLAYER_WON or result == RESULT_PLAYER_DEAD):
                sound_channel = None
                if (result == RESULT_PLAYER_WON):
                    #print("WON")
                    sound_channel = self.win_sound.play()
                else:
                    #print("LOSE")
                    sound_channel = self.lose_sound.play()

                #  wait for sound to end
                while sound_channel.get_busy() == True:
                    continue
                break
            else:
                pass
            
     

        #  return a tuple of
        #(number of collected toys, elapsed time step)
        return (self.collected_toy_count,
                self.elapsed_time_step,
                self.path_cost_so_far)



    def start_level_computer(self, level_index, agent, 
                             render=False, play_sound=False,
                             max_episode_length=150,
                             test=False):
        self.init_level(level_index)

        if (render):
            self.draw_level(self.current_level.get_matrix())

        #  number of all toys in the initial level configuration
        self.total_toy_count = len(self.toys)

        #  let the agent think
        t1 = time.time()
        sequence = agent.solve(self.current_level.get_matrix(), 
                               self.player.get_row(), self.player.get_col())
        t2 = time.time()
        elapsed_solve_time = t2-t1
        print("Decided sequence:")
        print(sequence)
        print("{} decided sequence length:{}".format(agent.__class__.__name__, len(sequence)))
        

        #  start playing the decided sequence
        for chosen_action in sequence:
            result = 0

            #  input source will use matrix to decide
            matrix = self.current_level.get_matrix()

       
            chosen_action = chosen_action  #sequence[self.elapsed_time_step]


            #  apply decided action
            result = self.step(chosen_action, render=render)


            #  if we want to render our agent, wait some time 
            if (render):
                self.clock.tick(FPS)
                pygame.event.get()

            #  check if game finished
            if (result == RESULT_PLAYER_WON or result == RESULT_PLAYER_DEAD):
                if (play_sound):
                    sound_channel = None
                    if (result == RESULT_PLAYER_WON):
                        sound_channel = self.win_sound.play()
                    else:
                        sound_channel = self.lose_sound.play()

                    #  wait for sound to end
                    while sound_channel.get_busy() == True:
                        continue
                break
            else:
                pass
             
            
            #  check if we reached episode length
            if (self.elapsed_time_step >= max_episode_length):
                break
        

        if (result != RESULT_PLAYER_WON):
            #  must be lose case for this homework
            if (play_sound):
                sound_channel = None
                sound_channel = self.lose_sound.play()

                #  wait for sound to end
                while sound_channel.get_busy() == True:
                    continue


        #  return a tuple of
        #(number of collected toys, elapsed time step)
        return (self.collected_toy_count,
                self.elapsed_time_step, elapsed_solve_time, result, self.path_cost_so_far)
    
