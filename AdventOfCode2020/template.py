"""
Template file to make it easier to copy the basic structure.
"""
import argparse
import os

class adapter_array():

    def __init__(self, input_list_path: str):
        """
        Handle the input file and store the contents in a class variable
        :param input_list_path (str): Path to the input file
        """
        # Verify the file exists
        if not os.path.exists(input_list_path):
            print(f"Input file does not exist: {input_list_path}")
            exit(1)

        # Parse the file and store it in a list
        with open(input_list_path, 'r') as f:
            # Store the lines of input into the self.input var
            self.input = f.readlines()

    def part_one_function(self):
        """
        Figure out ...
        """
        # Print the solution
        print("--------------------PART 1-----------------------")
        print(f"Answer: {1}")


    def part_two_function(self):
        """
        Figure out ...
        """
        
        # Print the solution
        print("--------------------PART 2-----------------------")
        print(f"Answer: {1}")


    def main(self, part_one: bool = True, part_two: bool = True):
        """
        Run part one, part two, or both and output the answers.
        """
        if part_one:
            self.part_one_function()
        
        if part_two:
            self.part_two_function()
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the program.")
    parser.add_argument("--input-path", help="Path to the input file", 
                        type=str, required=True)
    parser.add_argument("--skip-one", help="Skip part 1", 
                        action='store_true', required=False, default=False)
    parser.add_argument("--skip-two", help="Skip part 2", 
                        action='store_true', required=False, default=False)

    args = parser.parse_args()
    adapter = adapter_array(input_list_path=args.input_path)
    adapter.main(part_one=not args.skip_one, part_two=not args.skip_two)