from output_verifier import *
from bowl import write_output, light_bulbs
import sys

def light_cant_remove(board, i, j):
    SPECIAL_CHARS = ['X', '0', '1', '2', '3', '4', 'L']
    r = len(board)
    c = len(board[0])
    
    for x in range(j - 1, -1, -1):
        if board[i][x] in SPECIAL_CHARS:
            return False

    for x in range(j + 1, c):
        if board[i][x] in SPECIAL_CHARS:
            return False

    for y in range(i - 1, -1, -1):
        if board[y][j] in SPECIAL_CHARS:
            return False

    for y in range(i + 1, r):
        if board[y][j] in SPECIAL_CHARS:
            return False
    return True

def simple_greedy(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'L':
                if not light_cant_remove(board, i, j):
                    board[i][j] = '.'



def main():
    grid_dems, grid = get_input_data(sys.argv[1])
    grid = light_bulbs(grid)
    simple_greedy(grid)
    violations = determine_violations(grid)
    write_output(grid, violations)

if __name__ == "__main__":
    main()
