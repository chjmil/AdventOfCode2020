"""
Template file to make it easier to copy the basic structure.
"""
import argparse
import os

def main(input_list_path: str):
    """
    Parse through the provided file for ...
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

    # Print the solution
    print("--------------------PART 1-----------------------")
    print(f"Answer: {1}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the program.")
    parser.add_argument("--input-path", help="Path to the input file", 
                        type=str, required=True)

    args = parser.parse_args()
    main(input_list_path=args.input_path)