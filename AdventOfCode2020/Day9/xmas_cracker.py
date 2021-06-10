"""
Template file to make it easier to copy the basic structure.
"""
import argparse
import os
import itertools

def part_one(input: list, preamble: int):
    """
    Figure out which number doesn't belong
    :param input_list_path (str): Path to the input file
    :param preamble (int): number of values to account for
    :return value that doesn't belong 
    """
    cur_selection = input[:preamble]
    problem_num = 0

    for val in input[preamble:]:
        # list comprehension of the possible sums of the current_selection. 
        # Place them in a set to remove duplicates and make it smaller
        possible_values = set([x+y for x,y in list(itertools.combinations(cur_selection, r=2))])
        if val in possible_values:
            cur_selection.pop(0)
            cur_selection.append(val)
            continue
        problem_num = val
        break

    # Print the solution
    print("--------------------PART 1-----------------------")
    print(f"Answer: {problem_num}")


def main(input_list_path: str, preamble: int = 25):
    """
    Parse through the provided file to figure out which number doesn't belong in the list
    :param input_list_path (str): Path to the input file
    :param preamble (int): number of values to account for
    """
    # Verify the file exists
    if not os.path.exists(input_list_path):
        print(f"Input file does not exist: {input_list_path}")
        exit(1)

    # Parse the file and store it in a list
    with open(input_list_path, 'r') as f:
        # List comprehension to read in the values
        input = [int(x) for x in f.readlines()]

    part_one(input, preamble)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the program.")
    parser.add_argument("--input-path", help="Path to the input file", 
                        type=str, required=True)
    parser.add_argument("--preamble", help="Number of values to consider", 
                        type=int, required=False)
    

    args = parser.parse_args()
    if args.preamble:
        main(input_list_path=args.input_path, preamble=args.preamble)
    else:
        main(input_list_path=args.input_path)