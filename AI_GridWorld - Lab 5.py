# Grid World: AI-controlled play

# Instructions:
#   Move up, down, left, or right to move the character. The 
#   objective is to find the key and get to the door
#
# Control:
#    arrows  : Merge up, down, left, or right
#    s       : Toggle slow play
#    a       : Toggle AI player
#    d       : Toggle rendering 
#    r       : Restart game
#    q / ESC : Quit

from GridWorld import GridWorld
import numpy as np
import pygame
from collections import defaultdict 

from numpy import random

import scipy.stats as stats


# Initialize the environment
env = GridWorld()
env.reset()
x, y, has_key = env.get_state()

# Definitions and default settings
actions = ['left', 'right', 'up', 'down']
exit_program = False
action_taken = False
slow = True
runai = True
render = True
done = False

# Game clock
clock = pygame.time.Clock()

# INSERT YOUR CODE HERE (1/2)
# Define data structure for q-table and define the discount factor
q_table = defaultdict(lambda: [20 for i in range(4)])
epsilon = 0

total_count = 0
win_count = 0
different_discounts = [round(0.1 * item, 1) for item in range(2, 10)]
all_games = {round(key, 1): value for key, value in zip(different_discounts, [[] for i in different_discounts])}
index = 0

print(all_games)

# END OF YOUR CODE (1/2)

while not exit_program:

    if render:
        env.render()
    
    # Slow down rendering to 5 fps
    if slow and runai:
        clock.tick(5)       

    # Automatic reset environment in AI mode
    if done and runai:
        env.reset()
        x, y, has_key = env.get_state()
        done = False
        continue
        
    # Process game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                exit_program = True
            if event.key == pygame.K_UP:
                action, action_taken = 'up', True
            if event.key == pygame.K_DOWN:
                action, action_taken  = 'down', True
            if event.key == pygame.K_RIGHT:
                action, action_taken  = 'right', True
            if event.key == pygame.K_LEFT:
                action, action_taken  = 'left', True
            if event.key == pygame.K_r:
                env.reset()   
            if event.key == pygame.K_d:
                render = not render
            if event.key == pygame.K_s:
                slow = not slow
            if event.key == pygame.K_a:
                runai = not runai
                clock.tick(5)
    
    # AI controller (enable/disable by pressing 'a')
    if runai:
        # INSERT YOUR CODE HERE (2/2)
        #
        # Implement a Grid World AI (q-learning): Control the person by 
        # learning the optimal actions through trial and error
        #
        # The state of the environment is available in the variables
        #    x, y     : Coordinates of the person (integers 0-9)
        #    has_key  : Has key or not (boolean)
        #
        # To take an action in the environment, use the call
        #    (x, y, has_key), reward, done = env.step(action)
        #
        #    This gives you an updated state and reward as well as a Boolean 
        #    done indicating if the game is finished. When the AI is running, 
        #    the game restarts if done=True

        # 1. choose an action
        lastState = (x,y, has_key)
        action_index = q_table[lastState].index(max(q_table[lastState]))
        rando = np.random.random() > 1-epsilon
        # print(rando)
        action = actions[random.randint(4)] if rando else actions[action_index]
        # print(action)
        # 2. step the environment
        (x, y, has_key), reward, done = env.step(action)
        # 3. update q table
        current_discount = different_discounts[index]
        q_table[lastState][action_index] = reward + current_discount *max(q_table[(x,y,has_key)])
        # print(q_table)
        # print("__________")

        # Counters
        total_count += 1
        if reward == 100 and done:
            win_count += 1
        elif reward != 100 and done:
            win_count = 0
        if win_count == 5:
            env.reset()
            all_games[current_discount].append(total_count)
            # print(all_games)
            if len(all_games[current_discount]) == 5:
                print(current_discount)
            if len(all_games[current_discount]) >= 500:
                index += 1
                print(index)
                if index >= len(different_discounts):
                    env.close()
                    # print(all_games)
                    for key, value in all_games.items():
                        print(sum(value)/len(value))
                        print(stats.ttest_1samp(value, popmean=0).confidence_interval(confidence_level=0.95))
            q_table = defaultdict(lambda: [20 for i in range(4)])
            total_count = 0
            win_count = 0
        # END OF YOUR CODE (2/2)
    
    # Human controller        
    else:
        if action_taken:
            (x, y, has_key), reward, done = env.step(action)
            action_taken = False


env.close()
