import argparse
import os
import re

class bit_mask():

    def __init__(self, input_list_path: str):
        """
        Handle the input file and store the contents in a class variable
        :param input_list_path (str): Path to the input file
        """
        # Hold the current mask
        self.mask = ""
        # dictionary to hold the values in memory
        self.mem = dict()
        self.debug = False
        if os.environ.get('debug', False):
            self.debug = True

        # Verify the file exists
        if not os.path.exists(input_list_path):
            print(f"Input file does not exist: {input_list_path}")
            exit(1)

        # Parse the file and store it in a list
        with open(input_list_path, 'r') as f:
            # Store the lines of input into the self.input var
            self.input = [x.strip() for x in f.readlines()]

    def bitmask(self, val):
        """
        """
        # i feel like there needs to be a better way to use a bit mask

        # Get the binary value and pad it to match the mask
        bin_val = f"{bin(val).replace('0b', ''):0>{len(self.mask)}}"

        if self.debug:
            print(f"\nDEBUG: initial bin_val: {bin_val}")
        

        # loop through until the remaining mask is just Xs
        for i in range(len(self.mask)):
            if self.mask[i] == 'X':
                continue
            bin_val = bin_val[:i] + self.mask[i] + bin_val[i+1:]
        
        if self.debug:
            print(f"DEBUG: bin_val: {bin_val}")
        
        # convert back to decimal
        bin_val = int(bin_val, 2)
        if self.debug:
            print(f"DEBUG: final bin_val: {bin_val}")

        return bin_val

    def part_one_function(self):
        """
        Figure out the sum of the values in memory
        """
        structure = re.compile(r"mem\[(\d+)\] = (\d+)")
        # go line by line and either set the mask or the value
        for line in self.input:
            if 'mask' in line:
                self.mask = line[line.find(' = ')+3:].lstrip('X')
                continue
            values = structure.match(line)
            self.mem[values[1]] = self.bitmask(int(values[2]))

        if self.debug:
            print(f"DEBUG: mem: {self.mem}")

        # Print the solution
        print("--------------------PART 1-----------------------")
        print(f"Answer: {sum(self.mem.values())}")


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
    parser.add_argument("--debug", help="Print extra debugging info", 
                        action='store_true', required=False, default=False)

    args = parser.parse_args()
    if args.debug:
        os.environ['debug'] = "True"
    mask = bit_mask(input_list_path=args.input_path)
    mask.main(part_one=not args.skip_one, part_two=not args.skip_two)