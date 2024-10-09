import numpy as np
import sys
import os

from qinput import lightCells
from qinput import verify_bulb_count

# opens filename, returns expected violations and output grid
def readFile(filename):
    with open(filename, 'r') as file:
        # Read the first line to get the dimensions
        expected_violations = int(file.readline().strip())
        # Initialize an empty list to hold the rows
        grid = []
        
        # Read the next r lines
        for line in file:
            grid.append(list(line.strip()))
            
        # Convert the list into a numpy array
        np_grid = np.array(grid)

    return expected_violations, np_grid

# returns true / false if light bulb is a violation
def check_for_bulbs(grid, i, j):
    # set of blocking characters
    blocking = {'X', '0', '1', '2', '3', '4'}

    # define boundaries
    left_end = 0
    right_end = len(grid[i]) - 1
    top_end = 0
    bottom_end = grid.shape[0] - 1
    
    # check all cells left of bulb
    left_spot = j - 1
    while left_spot >= left_end:
        if grid[i][left_spot] == 'L':
            return True
        elif grid[i][left_spot] in blocking:
            # if bulb got blocked, break left loop
            break
        else:
            left_spot -= 1
    # check all cells right of bulb
    right_spot = j + 1
    while right_spot <= right_end:
        if grid[i][right_spot] == 'L':
            return True
        elif grid[i][right_spot] in blocking:
           break
        else:
            right_spot += 1
    # check all cells above bulb
    up_spot = i - 1
    while up_spot >= top_end:
        if grid[up_spot][j] == 'L':
            return True
        elif grid[up_spot][j] in blocking:
            break
        else:
            up_spot -= 1
    # check all cells below bulb
    down_spot = i + 1
    while down_spot <= bottom_end:
        if grid[down_spot][j] == 'L':
            return True
        elif grid[down_spot][j] in blocking:
            break
        else:
            down_spot += 1
    
    return False

# returns count of violations in grid
def get_violations(grid):
    # Use boolean matrix to ensure no double counting
    violations = np.full((len(grid), len(grid[0])), False, dtype=bool)

    # Iterate through the grid checking for violations
    numbered_cells = {'0','1','2','3','4'}

    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            curr_cell = grid[i][j]
            # If this cell is a numbered cell
            if(curr_cell in numbered_cells):
                # Ensure there is the required number of lightbulbs placed
                violations[i][j] = verify_bulb_count(grid, i, j, int(curr_cell))
            # If this cell is a lightbulb
            if(curr_cell == 'L'):
                # See if there are any unblocked lightbulbs in the same row or column
                violations[i][j] = check_for_bulbs(grid, i, j)

    count = np.sum(violations)

    return count

def verify(grid, expected_violations):

    # for 'L' in grid
        # call lightCells() on 'L'
    lights_idx = np.where(grid == 'L')
    for row, col in zip(lights_idx[0], lights_idx[1]):
        grid = lightCells(grid, row, col)

    # loop thru all cells
    for row in grid:
        for cell in row:
            # if blank cell exists (if cell == '.')
            if cell == '.':
                # return false; output is not valid
                print("OUTPUT INVALID: There are unlit cells in the grid.")
                return False
    
    # if we are here, there are no blank cells
    # call get_violations, compare to expected violations
    true_viols = get_violations(grid)
    if (true_viols == expected_violations):
        print("OUTPUT VALID")
        return True
    else:
        print(f"OUTPUT INVALID: expected {expected_violations} violations, found {true_viols} violations.")
        return False


    

def main():
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
        exp_viols, grid = readFile(arg1) 

    filenames = os.listdir('C:\\Users\\avalc\\OneDrive\\Desktop\\Algorithms\\algobowl\\outputs_extra')
    for file in filenames:
        exp_viols, grid = readFile('C:\\Users\\avalc\\OneDrive\\Desktop\\Algorithms\\algobowl\\outputs_extra\\' + file)
        print("-------------------------------------------------------")
        print("Verifying file: " + file)
        print(verify(grid, exp_viols))

if __name__ == "__main__":
    main()