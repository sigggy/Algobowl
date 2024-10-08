from currentAlg import *
import subprocess
import numpy as np
from pathlib import Path
import shutil
import sys


def collect_first_lines(directory):
    # List to store the integers
    first_line_values = []
    
    # Loop through each file in the directory using Path
    for filepath in directory.iterdir():
        if filepath.is_file():
            with filepath.open('r') as file:
                # Read the first line and strip any whitespace
                first_line = file.readline().strip()
                
                try:
                    # Convert the first line to an integer and add to the list
                    first_line_values.append(int(first_line))
                except ValueError:
                    print(f"Warning: Could not convert the first line of {filepath.name} to an integer.")

    return first_line_values


def main(input_file):
    input_file_path = Path(input_file)
    
    # Create the parent directory 'annealing_outputs' if it doesn't exist
    annealing_outputs_dir = Path("annealing_outputs")
    annealing_outputs_dir.mkdir(parents=True, exist_ok=True)
    
    # Run the algorithm 5 times
    for i in range(5):
        print(f"Executing run {i + 1} of 100..")
        subprocess.run(["python", "currentAlg.py", str(input_file_path)])
    
    # Create the output subdirectory using the input file name without extension
    output_subdir = annealing_outputs_dir / input_file_path.stem
    
    # Remove all files in the output subdirectory if it already exists
    if output_subdir.exists():
        for file in output_subdir.glob('*'):
            if file.is_file():
                file.unlink()  # Remove the file

    output_subdir.mkdir(parents=True, exist_ok=True)

    # Move all files from 'annealing_outputs' to the subdirectory
    for file in annealing_outputs_dir.glob('*'):
        if file.is_file():
            shutil.move(str(file), output_subdir)
    
    # Calculate the standard deviation of the first line values
    std = np.std(collect_first_lines(output_subdir))
    subprocess.run(f"echo {std} > {output_subdir}/T_val.txt", shell=True)


if __name__ == "__main__":
    main(sys.argv[1])
