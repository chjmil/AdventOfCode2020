"""
Template file to make it easier to copy the basic structure.
"""
import argparse
import os

def unique_answer_counter(group_list: list, *args):
    """
    Remove duplicates by creating a set and then return the length.
    This probably doesn't need to be its own function, but it might get
    expanded on in part 2.
    :param group_list (list): List of all answer choices for the group
    :return Number of unique answers
    """
    print(f"Group: {group_list}")
    num = len(set(group_list))
    print(f"Number of uniques: {num}")
    return num

def common_answer_counter(group_list: list, group_counter: int):
    """
    Return the number of answers that everyone answered yes to.
    :param group_list (list): List of all answer choices for the group
    :param group_counter (int): number of people in the group
    :return Number of common answers
    """
    print(f"Group: {group_list}")
    print(f"Group Count: {group_counter}")
    num = 0
    for char in set(group_list):
        # for every unique answer, see if the list contains group_counter number of answers 
        if group_counter == group_list.count(char):
            num += 1
    print(f"Number of common: {num}")
    return num


def main(input_list_path: str, unique: bool = False):
    """
    Parse through the provided file for groups of answers and sum them up.
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
    
    if unique:
        func = unique_answer_counter
    else:
        func = common_answer_counter

    total = 0
    current_group = []
    # count the number of people in the group
    group_counter = 0
    for i in input:
        # if it is an empty line, that is the end of this entry
        if i == '\n':
            total += func(current_group, group_counter)
            current_group = []
            group_counter = 0
            continue
        # break apart the line into it's answers
        current_group.extend([c for c in i.strip()])
        group_counter += 1

    
    # If there isn't a newline at the end of the file, run the answer_counter one last time
    if current_group is not []:
        total += func(current_group, group_counter)

    # Print the solution
    print("--------------------ANSWER-----------------------")
    print(f"Answer: {total}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the program.")
    parser.add_argument("--input-path", help="Path to the input file", 
                        type=str, required=True)
    parser.add_argument("--unique", help="Count the unique answers", 
                        action='store_true', required=False, default=False)

    args = parser.parse_args()
    main(input_list_path=args.input_path, unique=args.unique)