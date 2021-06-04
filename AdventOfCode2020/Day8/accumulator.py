"""
Template file to make it easier to copy the basic structure.
"""
import argparse
import os


visited_lines = set()

def next_line(input: str, line_number: int):
    """
    Execute the next line
    """
    line = input[line_number]
    instruction, accum = line.split(' ')
    accum = int(accum)

    current_len = len(visited_lines)
    visited_lines.add(line_number)
    if current_len == len(visited_lines):
        print("Detecting infinite loop. Exiting...")
        return 0
    
    print(line)

    if instruction == 'acc':
        return next_line(input, line_number+1) + accum
    elif instruction == 'jmp':
        return next_line(input, line_number+accum)
    else:
        return next_line(input, line_number+1)




def last_acc_value(input: list):
    """
    Find the final value of the accumulator before it begins the 
    infinite loop.
    :param input (list): list of instructions to read through
    """
    accumulator = 0
    accumulator = next_line(input, 0)

    # Print the solution
    print("--------------------PART 1-----------------------")
    print(f"Answer: {accumulator}")


def main(input_list_path: str, part_one: bool):
    """
    Parse through the provided file for the list of instructions
    :param input_list_path (str): Path to the input file
    """
    # Verify the file exists
    if not os.path.exists(input_list_path):
        print(f"Input file does not exist: {input_list_path}")
        exit(1)

    # Parse the file and store it in a list
    with open(input_list_path, 'r') as f:
        # List comprehension to ...
        input = [x for x in f.readlines()]

    if part_one:
        last_acc_value(input)
        exit(0)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the program.")
    parser.add_argument("--input-path", help="Path to the input file", 
                        type=str, required=True)
    parser.add_argument("--part1", help="Run the program in respect to part 1", 
                        action="store_true", dest="part_one")
    parser.add_argument("--part2", help="Run the program in respect to part 2", 
                        action="store_false", dest="part_one")

    args = parser.parse_args()
    main(input_list_path=args.input_path, part_one=args.part_one)