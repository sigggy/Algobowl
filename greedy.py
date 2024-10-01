from output_verifier import *
from bowl import write_output, light_bulbs
import random
import sys

def validate_illuminated_cells(grid: List[List[str]], r: int, c: int) -> List[List[str]]:
    SPECIAL_CHARS = ['X', '0', '1', '2', '3', '4', 'L']
    illuminated_grid = [row[:] for row in grid]

    for i in range(r):
        for j in range(c):
            if grid[i][j] == 'L':
                # Illuminate left
                for x in range(j - 1, -1, -1):
                    if grid[i][x] in SPECIAL_CHARS:
                        break
                    illuminated_grid[i][x] = '*'

                # Illuminate right
                for x in range(j + 1, c):
                    if grid[i][x] in SPECIAL_CHARS:
                        break
                    illuminated_grid[i][x] = '*'

                # Illuminate up
                for y in range(i - 1, -1, -1):
                    if grid[y][j] in SPECIAL_CHARS:
                        break
                    illuminated_grid[y][j] = '*'

                # Illuminate down
                for y in range(i + 1, r):
                    if grid[y][j] in SPECIAL_CHARS:
                        break
                    illuminated_grid[y][j] = '*'
  
    for i in range(r):
        for j in range(c):
            if illuminated_grid[i][j] == '.':
                return False 
    return True

def greedy(board, i, j):
    if board[i][j] == 'L':
        board[i][j] = '.' # remove light-bulb
        if not validate_illuminated_cells(board, len(board), len(board[0])):
            board[i][j] = 'L' # put back if not possible

def greedy_left_right_top_bottom(board): # 
    for i in range(len(board)):
        for j in range(len(board[i])):
            greedy(board, i , j)

def greedy_random_order(board): # random order
    indexes = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            indexes.append((i, j))
    random.shuffle(indexes)
    for i, j in indexes:
        greedy(board, i, j)
        
def greedy_alternating_rows(board): # alternate rows
    t, b = 0, len(board) - 1
    count = 0
    while (t < b):
        if count % 2 == 0:
            for j in range(len(board[0])):
                greedy(board, t, j)
            t += 1
        else:
            for j in range(len(board[0])):
                greedy(board, b, j)
            b -= 1
        count += 1

def greedy_alt_row_col(board):
    num_rows = len(board)
    num_cols = len(board[0])

    num = min(num_rows, num_cols)

    for x in range(num):
        for j in range(num_cols):
            greedy(board, x, j)
        for i in range(num_rows):
            greedy(board, i, x)
    
    # check remaining rows or columns
    for i in range(num_rows - num):
        for j in range(num_cols):
            greedy(board, num + i, j)
    
    for j in range(num_cols - num):
        for i in range(num_rows):
            greedy(board, i, num + j)

def main():
    grid_dems, grid = get_input_data(sys.argv[1])
    grid = light_bulbs(grid)
    greedy_random_order(grid)
    violations = determine_violations(grid)
    write_output(grid, violations)

if __name__ == "__main__":
    main()
