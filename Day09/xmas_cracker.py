import argparse
import os
import itertools

def xmas_crack(input: list, preamble: int):
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

    # begin part 2
    contiguous_set = []
    counter = 0
    for val in input:
        counter += val
        contiguous_set.append(val)
        while counter > problem_num:
            # pop the oldest and redo the counter. Repeat if it's still too large
            contiguous_set.pop(0)
            counter = sum(contiguous_set)
        if counter == problem_num:
            # found the set. Break out of loop
            break

    
    print("--------------------PART 2-----------------------")
    print(f"List of contiguous values: {contiguous_set}")
    contiguous_set.sort()
    print(f"Smallest: {contiguous_set[0]}")
    print(f"Largest: {contiguous_set[-1]}")

    print(f"Answer: {contiguous_set[0] + contiguous_set[-1]}")





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

    xmas_crack(input, preamble)


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