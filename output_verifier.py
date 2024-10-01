# flake8: noqa
import sys
import copy
from typing import List, Tuple



def get_input_data(file_path: str) -> Tuple[List[int], List[List[str]]]:
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()  # Read all lines from the file
    grid_dems = list(map(int, lines[0].strip().split()))  # Parse dimensions from the first line
    grid = [list(line.strip()) for line in lines[1:] if line.strip()]  # Convert each line into a list of characters
    
    return grid_dems, grid


def print_grid(grid: List[List[str]]) -> None:
    for row in grid:
        print(" ".join(row))

def validate_input_and_output(grid1: List[List[str]], grid2: List[List[str]]):
        special_chars = ['X', '0', '1', '2', '3', '4']
        
        for row in range(len(grid1)):
            for entry in range(len(grid1[row])):
                if grid1[row][entry] in special_chars:
                    if grid1[row][entry] != grid2[row][entry]:
                            print(grid1[row][entry])
                            print(grid2[row][entry])
                            print("---------------------------------------------------------------------")
                            print("False")
                            print("There graph structure does not match ")
                            print("The Graph is Invalid")
                            print("---------------------------------------------------------------------")
                            exit(1)
        return 

def validate_graphs_dems(grid1_dems, grid1, grid2):
    # Get the actual dimensions of the grids
    actual_grid1_dems = [len(grid1), len(grid1[0])] if grid1 else [0, 0]
    actual_grid2_dems = [len(grid2), len(grid2[0])] if grid2 else [0, 0]

    # Check if all three dimension lists are the same

    if not grid1_dems == actual_grid1_dems == actual_grid2_dems:
        print(grid1_dems)
        print(actual_grid1_dems)
        print(actual_grid2_dems)
        print("---------------------------------------------------------------------")
        print("False")
        print("There is a issue with the dimensions")
        print("The Graph is Invalid")
        print("---------------------------------------------------------------------")
        exit(1)

from typing import List, Tuple

from typing import List

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


    #now check for validity    
    for i in range(r):
        for j in range(c):
            if illuminated_grid[i][j] == '.':
                print("Illuminated Grid")
                print("---------------------------------------------------------------------")
                print_grid(illuminated_grid)
                print("---------------------------------------------------------------------")
                print('\n' * 2)
                print(f' Issue found at ({i}, {j})')  
                print('\n' * 2)
                print("---------------------------------------------------------------------")
                print("False")
                print("There is a unlit cell")
                print("The Graph is Invalid")
                print("---------------------------------------------------------------------")
                exit(1)
    
    print("Illuminated Grid")
    print("---------------------------------------------------------------------")
    print_grid(illuminated_grid)
    print("---------------------------------------------------------------------")
    return     

def apply_light_violations(grid: List[List[str]], grid_copy: List[List[str]], directions):
    rows, cols = len(grid), len(grid[0])
    # Iterate through each cell in the grid
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 'L':
                # For each light, check all four directions
                for direction in directions.values():
                    dr, dc = direction
                    r, c = row + dr, col + dc
                    while 0 <= r < rows and 0 <= c < cols:
                        if grid[r][c] != '.':
                            if grid[r][c] == 'L':
                                grid_copy[r][c] = 'V'
                            break
                        r += dr
                        c += dc

def apply_numeric_violations(grid: List[List[str]], grid_copy: List[List[str]], directions) -> None:
    rows, cols = len(grid), len(grid[0])
    # Iterate through each cell in the grid
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != '.' and grid[row][col] != "L" and grid[row][col] != "X":
                val = int(grid[row][col])
                # For each light, check all four directions
                count = 0
                for direction in directions.values():
                    dr, dc = direction
                    r, c = row + dr, col + dc
                    # Check only one tile over
                    if 0 <= r < rows and 0 <= c < cols:
                        if grid[r][c] == 'L':
                            count += 1
                # If the count of lights is not equal to the expected value, mark as violation
                if count != val:
                    grid_copy[row][col] = 'V'
                    

def determine_violations(grid: List[List[str]]) -> int:
    grid_copy = copy.deepcopy(grid)
    directions = {
        'left': (0, -1),
        'right': (0, 1),
        'up': (-1, 0),
        'down': (1, 0)
    }
    apply_light_violations(grid, grid_copy, directions)
    apply_numeric_violations(grid, grid_copy, directions)
    
    print('\n' * 2)
    print("Violation Grid")
    print("---------------------------------------------------------------------")
    print_grid(grid_copy)
    print("---------------------------------------------------------------------")
    violations =  sum(row.count('V') for row in grid_copy)
    print('\n' * 2)
    print("---------------------------------------------------------------------")
    print(f'{violations} violations were found in the output graph')
    print("---------------------------------------------------------------------")
    return violations

def validate_violations(assumed_violations, grid): 
    calculated_violations = determine_violations(grid)
    if assumed_violations != calculated_violations:
        print('\n' * 2)
        print("---------------------------------------------------------------------")
        print("False")
        print("There is a violation mismatch")
        print(f'The graph report {assumed_violations} violations')
        print(f'Out verifier fround {calculated_violations} violations')
        print("The Graph is Invalid")
        print("---------------------------------------------------------------------")
        exit(1)
    return 




def main(input_file1: str, input_file2: str) -> None:
    # Read the input files into 2D grids
    grid1_dems, grid1 = get_input_data(input_file1)
    grid2_dems, grid2 = get_input_data(input_file2)



    # Print the 2D grids to verify the contents
    print()
    print("Input Grid (Grid 1):")
    print("---------------------------------------------------------------------")
    print_grid(grid1)
    print("---------------------------------------------------------------------")
    print('\n')
    print("\nOutput Grid (Grid2):")
    print("---------------------------------------------------------------------")
    print_grid(grid2)
    print("---------------------------------------------------------------------")
    print('\n')  


    validate_graphs_dems(grid1_dems,grid1,grid2)
    validate_input_and_output(grid1,grid2)
    validate_illuminated_cells(grid2, len(grid2), len(grid2[0]))
    validate_violations(grid2_dems[0], grid2)
    print("---------------------------------------------------------------------")
    print(f'The graph is valid')
    print("---------------------------------------------------------------------")



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file1> <input_file2>")
        sys.exit(1)

    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]

    main(input_file1, input_file2)
