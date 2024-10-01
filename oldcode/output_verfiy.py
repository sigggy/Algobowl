# flake8: noqa
import sys
import os
from typing import List, Tuple
import copy

def get_input_data() -> Tuple[List[int], List[List[str]]]:
    lines = sys.stdin.read().splitlines()
    grid_dims = list(map(int, lines[0].strip().split()))
    grid = [list(line.strip()) for line in lines[1:] if line.strip()]
    
    return grid_dims, grid

def get_unique_output_path() -> str:
    os.makedirs("outputs", exist_ok=True)
    
    file_number = 1
    while True:
        output_path = os.path.join("outputs", f"output{file_number}.txt")
        if not os.path.exists(output_path):
            return output_path
        file_number += 1

def write_output(grid: List[List[str]], violations: int) -> None:
    output_path = get_unique_output_path()
    with open(output_path, 'w') as file:
        file.write(str(violations) + '\n')
        for row in grid:
            row_to_write = " ".join(row)
            file.write(row_to_write + '\n')
    print(f"Output written to: {output_path}")

def light_bulbs(grid: List[List[str]]) -> List[List[str]]:
    for row in range(len(grid)):
        for entry in range(len(grid[row])):
            if grid[row][entry] == '.':
                grid[row][entry] = 'L'
    return grid

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
    return sum(row.count('V') for row in grid_copy)


def main() -> None:
    grid_dims, grid = get_input_data()
    violations = determine_violations(grid)
    print(violations)


if __name__ == "__main__":
    main()

