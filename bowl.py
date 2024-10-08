# flake8: noqa
import sys
import os
from typing import List, Tuple

def get_input_data() -> Tuple[List[int], List[List[str]]]:
    lines = sys.stdin.read().splitlines()
    grid_dems = list(map(int, lines[0].strip().split()))
    grid = [list(line.strip()) for line in lines[1:] if line.strip()]
    
    return grid_dems, grid

def get_unique_output_path() -> str:
    os.makedirs("outputs", exist_ok=True)
    
    file_number = 1
    while True:
        output_path = os.path.join("annealing_outputs", f"output{file_number}.txt")
        if not os.path.exists(output_path):
            return output_path
        file_number += 1

def write_output(grid: List[List[str]], violations: int) -> None:
    output_path = get_unique_output_path()
    with open(output_path, 'w') as file:
        file.write(str(violations) + '\n')
        for row in grid:
            row_to_write = ''.join(row)
            file.write(row_to_write + '\n')
    print(f"Output written to: {output_path}")

def light_bulbs(grid: List[List[str]]) -> List[List[str]]:
    for row in range(len(grid)):
        for entry in range(len(grid[row])):
            if grid[row][entry] == '.':
                grid[row][entry] = 'L'
    return grid

def determine_violations(grid: List[List[str]]) -> int:
    return 1

def main() -> None:
    grid_dems, grid = get_input_data()
    lit_grid = light_bulbs(grid)
    violations = determine_violations(lit_grid)
    write_output(lit_grid, violations)

if __name__ == "__main__":
    main()

