import argparse
from time import time, sleep
import os
from types import FunctionType

def for_loop(input_list: list):
    """
    For loop through the list to see if any match. I'm worried that this 
    might be slow.
    :param input_list (List): List of input values

    Result from running it:
        Found combo: 1917 & 103
        Results:
        Answer: 197451
        Time: 0.0004508495330810547
    """
    # Search for values from current value to end of list.
    for i in range(len(input_list)):
        current_val = input_list[i]
        for val in input_list[i+1:]:
            if current_val + val == 2020:
                print(f"Found combo: {current_val} & {val}")
                return current_val * val

def for_loop_three(input_list: list):
    """
    For loop through the list to see if any three entries match.
    :param input_list (List): List of input values

    Result from running it:
        Found combo: 443 & 232 & 1345
        Results:
        Answer: 138233720
        Time: 0.06270599365234375
    """
    # Search for values from current value to end of list.
    for i in range(len(input_list)):
        first_val = input_list[i]
        for j in range(len(input_list[i:])):
            second_val = input_list[j]
            for val in input_list[j+1:]:
                if first_val + second_val + val == 2020:
                    print(f"Found combo: {first_val} & {second_val} & {val}")
                    return first_val * second_val * val


def search(input_list: list):
    """
    Take the value and search through the list for 2020-x to see if it exists.
    If so, multiply it against the first value and return it.
    :param input_list (List): List of input values

    Result from running it:
        Found combo: 1917 & 103
        Results:
        Answer: 197451
        Time: 0.0009980201721191406
    """
    for val in input_list:
        if 2020-val in input_list:
            print(f"Found combo: {val} & {2020-val}")
            return (2020-val) * val

def main(input_list_path: str):
    """
    Search through the provided file for two entries that sum to 2020. Take those numbers, 
    multiply them together, and return the result.
    :param input_list_path (str): 
    """
    # Verify the file exists
    if not os.path.exists(input_list_path):
        print(f"Input file does not exist: {input_list_path}")
        exit(1)

    # Parse the file and store it in a list
    with open(input_list_path, 'r') as f:
        # List comprehension to convert strings in the file to ints
        input = [int(x) for x in f.readlines()]
    
    def performance_check(function_pointer: FunctionType):
        """
        Fun little method to check the performance of each function.
        Not necessary for the actual expense_report, but it's fun to 
        see which one runs faster.
        :param function_pointer (FunctionType): Pointer to the function to test
        """
        start_time = time()
        answer = function_pointer(input)
        end_time = time()

        print(
            "Results:\n"
            f"Answer: {answer}\n"
            f"Time: {end_time-start_time}\n"
        )
    
    print("Running the For Loop function...")
    performance_check(for_loop)
    print("Running the Search function...")
    performance_check(search)

    print("-----------------PART 2---------------")
    print("Running the For Loop function...")
    performance_check(for_loop_three)



    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process the expense report.")
    parser.add_argument("--input-path", help="Path to the expense report values", 
                        type=str, required=True)

    args = parser.parse_args()
    main(input_list_path=args.input_path)