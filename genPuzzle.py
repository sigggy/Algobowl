import random
import numpy as np

def generate_akari_puzzle(r, c, gray_ratio=0.2): # TODO: seed puzzles
    grid = np.full((r, c), '.', dtype=str)
        
    num_gray = int(gray_ratio * r * c)
    gray_positions = random.sample(range(r * c), num_gray)
        
    for pos in gray_positions:
        row, col = divmod(pos, c)
        grid[row, col] = 'X'
        
    for pos in gray_positions:
        if random.random() < 0.3:
            row, col = divmod(pos, c)
            grid[row, col] = str(random.randint(0, 4))
        
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
        if r * c > 10**5:
            print(f"This is not a valid puzzle") # make sure we don't fuck up
            continue
        print(f"Generating puzzle of size {r}x{c}...")
        puzzle = generate_akari_puzzle(r, c, gray_ratio=0.2)
        save_puzzle_to_file(puzzle, f'puzzles/akari_puzzle{r}x{c}.txt') # TODO: save puzzles to a unique file name

if __name__ == "__main__":
    main()
