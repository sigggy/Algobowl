import random
import numpy as np

def generate_akari_puzzle(r, c, gray_ratio=0.2, seed=None):
    assert 1 <= r * c <= 10**5, "Grid size must satisfy 1 ≤ r × c ≤ 10^5"

    # Create a local random generator instance with the given seed
    rng = random.Random(seed)

    grid = np.full((r, c), '.', dtype=str)
        
    num_gray = int(gray_ratio * r * c)
    all_positions = list(range(r * c))
    gray_positions = rng.sample(all_positions, num_gray)
        
    for pos in gray_positions:
        row, col = divmod(pos, c)
        grid[row, col] = 'X'
        
    for pos in gray_positions:
        if rng.random() < .3:
            row, col = divmod(pos, c)
            grid[row, col] = str(rng.randint(0, 4))
        
    return [''.join(row) for row in grid]

def save_puzzle_to_file(puzzle, filename):
    with open(filename, 'w') as f:
        f.write(f'{len(puzzle)} {len(puzzle[0])}\n')
        for row in puzzle:
            f.write(row + '\n')

def main():
    
    puzzle_sizes = [
        (10, 10), 
        (100, 100), 
        (300, 300), 
    ]
    
    for r, c in puzzle_sizes:
        seed = random.random() * 10**5 # get large random seed
        if r * c > 10**5:
            print(f"This is not a valid puzzle") # make sure we don't fuck up
            continue
        print(f"Generating puzzle of size {r}x{c}...")
        puzzle = generate_akari_puzzle(r, c, gray_ratio=0.2, seed=seed)
        save_puzzle_to_file(puzzle, f'inputs/akari_puzzle<{r}x{c}>{seed}.txt') # write puzzle with seed

if __name__ == "__main__":
    main()
