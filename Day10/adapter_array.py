import argparse
import os
from copy import deepcopy
from itertools import permutations

class adapter_array():

    def __init__(self, input_list_path: str):
        """
        Handle the input file and store the contents in a class variable
        :param input_list_path (str): Path to the input file
        """
        # Variables to store the jolt-differences
        self.one_jolt: int = 0
        self.two_jolt: int = 0
        # Set three_jolt to 1 since the final one is always +3
        self.three_jolt: int = 1

        # Verify the file exists
        if not os.path.exists(input_list_path):
            print(f"Input file does not exist: {input_list_path}")
            exit(1)

        # Parse the file and store it in a list
        with open(input_list_path, 'r') as f:
            # List comprehension to read in all joltages
            self.input = [int(x) for x in f.readlines()]

    def part_one_function(self):
        """
        Figure out the number of 1-jolt differences and 3-jolt
        differences from the adapter array.
        """
        sorted_list = deepcopy(self.input)
        sorted_list.sort()
        current_jolt = 0
        for adapter in sorted_list:
            if adapter-current_jolt == 1:
                self.one_jolt += 1
            elif adapter-current_jolt == 2:
                self.two_jolt += 1
            elif adapter-current_jolt == 3:
                self.three_jolt += 1
            else:
                print(f"Something went wrong: Adapter: {adapter}\nCurrent: {current_jolt}")
            current_jolt = adapter

        # Print the solution
        print("--------------------PART 1-----------------------")
        print(f"One Jolts: {self.one_jolt}")
        print(f"Two Jolts: {self.two_jolt}")
        print(f"Three Jolts: {self.three_jolt}")
        print(f"Answer: {self.one_jolt * self.three_jolt}")


    def part_two_function(self):
        """
        Figure out how many permutations there are that still meet the adapter criteria
        """
        sorted_list = deepcopy(self.input)
        sorted_list.sort()
        sorted_list.insert(0,0)
        sorted_list.append(sorted_list[-1]+3)

        # store the values of already-solved paths
        self.solved_paths = {}

        def dynamic_search(index: int):
            """
            Recursively figure out the number of adapter chains. Use Dynamic
            Programming to cut down the run time
            """
            if index == len(sorted_list)-1:
                return 1
            if index in self.solved_paths:
                return self.solved_paths[index]
            num = 0
            for i in range(index+1, len(sorted_list)):
                if sorted_list[i]-sorted_list[index] <= 3:
                    num += dynamic_search(i)
            
            self.solved_paths[index] = num
            return num

        # Print the solution
        print("--------------------PART 2-----------------------")
        print(f"Answer: {dynamic_search(0)}")


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