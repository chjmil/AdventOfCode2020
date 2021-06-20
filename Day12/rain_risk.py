import argparse
import os
from enum import Enum

class Compass(Enum):
    """
    Enum to hold all of the possible
    """
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3
    ROTATE = 90



class rain_risk():

    def __init__(self, input_list_path: str):
        """
        Handle the input file and store the contents in a class variable
        :param input_list_path (str): Path to the input file
        """
        self.debug = False
        self.position = [0,0]
        self.waypoint = None
        self.direction = Compass.EAST
        self.operations = {
            'E': lambda num: self.east(num),
            'S': lambda num: self.south(num),
            'W': lambda num: self.west(num),
            'N': lambda num: self.north(num),
            'R': lambda num: self.rotate(num),
            'L': lambda num: self.rotate(-num),
            'F': lambda num: self.forward(num),
        }

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

    # Functions to handle movement
    def east(self, num):
        if self.waypoint:
            self.waypoint[0] += num
        else:
            self.position[0] += num
    def west(self, num):
        if self.waypoint:
            self.waypoint[0] -= num
        else:
            self.position[0] -= num
    def north(self, num):
        if self.waypoint:
            self.waypoint[1] += num
        else:
            self.position[1] += num
    def south(self, num):
        if self.waypoint:
            self.waypoint[1] -= num
        else:
            self.position[1] -= num
    def rotate(self, num):
        # positive is clockwise
        old_direction = self.direction
        self.direction = Compass((self.direction.value + num/Compass.ROTATE.value)%4)
        # Rotate around the axis
        if self.waypoint:
            while old_direction.value != self.direction.value:
                self.waypoint.reverse()
                self.waypoint[1] *= -1
                old_direction = Compass((old_direction.value +1 )%4)

    def forward(self, num):
        if self.waypoint:
            self.position[0] += self.waypoint[0] * num
            self.position[1] += self.waypoint[1] * num
            return
        if self.direction.value == 0:
            self.east(num)
        elif self.direction.value == 1:
            self.south(num)
        elif self.direction.value == 2:
            self.west(num)
        else:
            self.north(num)


    def part_one_function(self):
        """
        Figure out the manhattan distance from start to finish
        """
        for direction in self.input:
            self.operations[direction[0]](int(direction[1:]))

        # Print the solution
        print("--------------------PART 1-----------------------")
        print(f"Answer: {abs(self.position[0]) + abs(self.position[1])}")


    def part_two_function(self):
        """
        Figure out ...
        """
        self.waypoint = [10,1]
        for direction in self.input:
            self.operations[direction[0]](int(direction[1:]))

        # Print the solution
        print("--------------------PART 2-----------------------")
        print(f"Answer: {abs(self.position[0]) + abs(self.position[1])}")


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
    program = rain_risk(input_list_path=args.input_path)
    program.main(part_one=not args.skip_one, part_two=not args.skip_two)