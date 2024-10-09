from output_verifier import *
from bowl import write_output, light_bulbs
import numpy as np
import random

def illuminate_from_light(light_map, i , j):
    r = len(light_map)
    c = len(light_map[0])

    for x in range(j - 1, -1, -1):
        if light_map[i][x] == -1:
            break
        light_map[i][x] += 1
                
    for x in range(j, c): # check light at location
        if light_map[i][x] == -1:
            break
        light_map[i][x] += 1
                
    for y in range(i - 1, -1, -1):
        if light_map[y][j] == -1:
            break
        light_map[y][j] += 1
               
    for y in range(i + 1, r):
        if light_map[y][j] == -1:
            break
        light_map[y][j] += 1

def create_lit_map(lit_map, board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] in ['X', '0', '1', '2', '3', '4']:
                lit_map[i][j] = -1
    for i in range(len(board)):
        for j in range(len(board[0])):      
            if board[i][j] == 'L':
                illuminate_from_light(lit_map, i, j) # allow to use greedy smart on board w lights

def greedy_smart(board): # takes empty board
    lit_map = np.zeros((len(board), len(board[0])))

    create_lit_map(lit_map, board)

    for i in range(len(lit_map)): # top-bottom-left-right
        for j in range(len(lit_map[0])):
            if lit_map[i][j] == 0:
                board[i][j] = 'L'
                illuminate_from_light(lit_map, i , j)

def validate_board(board, order, goodLights, badLights):
    lit_map = np.zeros((len(board), len(board[0])))

    create_lit_map(lit_map, board)

    for i, j in order[0]:
        if lit_map[i][j] == 0:
            board[i][j] = 'L'
            goodLights.append((i, j))
            illuminate_from_light(lit_map, i , j)
    for i, j in order[1]:
        if lit_map[i][j] == 0:
            board[i][j] = 'L'
            badLights.append((i, j))
            illuminate_from_light(lit_map, i , j)
    
    return goodLights, badLights

def greedy_smart_random(board):
    lit_map = np.zeros((len(board), len(board[0])))

    create_lit_map(lit_map, board)

    indexes = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            indexes.append((i, j))
    random.shuffle(indexes)
    for i, j in indexes:
        if lit_map[i][j] == 0:
            board[i][j] = 'L'
            illuminate_from_light(lit_map, i , j)

def main():
    _, light_map = get_input_data(sys.argv[1])
    greedy_smart_random(light_map)
    violations = determine_violations(light_map)
    write_output(light_map, violations)

if __name__ == "__main__":
    main()