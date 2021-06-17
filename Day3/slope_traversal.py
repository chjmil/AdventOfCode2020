import argparse
import os
from copy import deepcopy

def traverse(input, slope):

    # Set the coordinate values
    current_x_coord = 0
    x_slope = slope[0]
    y_slope = slope[1]
    max_x = len(input[0])-1
    tree_count = 0

    for y in range(len(input)):
        if y % y_slope != 0:
            continue
        if input[y][current_x_coord] == '#':
            tree_count += 1
            replace_char = 'X'
        else:
            replace_char = 'O'
        # update the graph to show if it was a hit or a miss
        input[y] = input[y][:current_x_coord  ]+ replace_char + input[y][current_x_coord+1:]
        current_x_coord = (current_x_coord + x_slope) % max_x
    
    for i in input:
        print(i.replace('\n', ''))

    
    return tree_count

def main(input_list_path: str, slope: tuple = (3,1)):
    """
    Parse through the input to see how many trees are hit 
    while going at the specified slope
    :param input_list_path (str): 
    :param slope (tuple): Slope of the toboggan
    """
    # Verify the file exists
    if not os.path.exists(input_list_path):
        print(f"Input file does not exist: {input_list_path}")
        exit(1)

    # Parse the file and store it in a list
    with open(input_list_path, 'r') as f: 
        input = f.readlines()
    
    slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]

    tree_hits = 0
    tree_mult = 1
    for slope in slopes:
        # Print the solution
        print(f"----------------Slope {slope}------------------")
        tree_hits = traverse(deepcopy(input), slope)
        print(f"Answer: {tree_hits}\n\n")
        tree_mult *= tree_hits
    
    print(f"Tree hits multiplied together: {tree_mult}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traverse the input file and hit some trees.")
    parser.add_argument("--input-path", help="Path to the input file", 
                        type=str, required=True)
    parser.add_argument("--slope", help="Slope to traverse at. Pass as two separate values ex. 3 1", 
                        type=int, nargs=2, required=False, default=(3,1))

    args = parser.parse_args()
    slope = tuple(args.slope)
    main(input_list_path=args.input_path, slope=slope)