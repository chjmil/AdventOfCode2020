import argparse
import os
import operator

class seating_system():

    def __init__(self, input_list_path: str):
        """
        Handle the input file and store the contents in a class variable
        :param input_list_path (str): Path to the input file
        """
        self.grid = None
        self.col_len = None
        self.row_len = None
        self.debug = False

        # Verify the file exists
        if not os.path.exists(input_list_path):
            print(f"Input file does not exist: {input_list_path}")
            exit(1)

        # Parse the file and store it in a list
        with open(input_list_path, 'r') as f:
            # Store the lines of input into the self.grid var
            raw_input = f.read()
            # if every seat is empty, replace them all as occupied to skip
            # first iteration
            if '#' not in raw_input:
                raw_input = raw_input.replace('L', '#')
            # Remove the last empty line
            self.grid = raw_input.split('\n')[:-1]
        # Number of rows
        self.row_len = len(self.grid)
        # Number of seats (columns)
        self.col_len = len(self.grid[0])

        if os.environ.get('debug', False):
            self.debug = True
    
    def step(self, seat: tuple):
        """
        Simulate the next round to see if the seat
        changes or stays the same.
        :param id (tuple): (x, y) coordinate
        """
        y_range = [max(seat[0]-1, 0), min(seat[0]+1, self.row_len-1)]
        x_range = [max(seat[1]-1, 0), min(seat[1]+1, self.col_len-1)]
        is_occupied = self.grid[seat[0]][seat[1]] == '#'
        if self.debug:
            print(f"\nDEBUG: id: {seat}. Char: {self.grid[seat[0]][seat[1]]}")
            print(f"DEBUG: x_range: {x_range}, y_range: {y_range}")

        # Wacky way to count the number of neighbors
        neighbors = ""
        i = y_range[0]
        while i <= y_range[1]:
            if self.debug:
                print(f"DEBUG: Neighbors: {self.grid[i][x_range[0]:x_range[1]+1]}")
            neighbors += self.grid[i][x_range[0]:x_range[1]+1]
            i+=1

        # Replace the current seat with a space so that it isn't counted
        neighbors = neighbors.replace(self.grid[seat[0]][seat[1]], '_', 1)
        if self.debug:
            print(f"DEBUG: Final neighbors: {neighbors}")

        num_neighbors = neighbors.count('#')
        if self.debug:
            print(f"DEBUG: Neighbor count: {num_neighbors}")
        if is_occupied:
            # if neighbors > 3, return L. else return #
            if num_neighbors > 3:
                return 'L'
            return '#'
        else:
            # if neighbors > 1, return L. else return #
            if num_neighbors == 0:
                return '#'
            return 'L'
        

    def part_one_function(self):
        """
        Figure out the number of occupied seats after the simulation
        has settled.
        """
        # step through until the previous grid is identical to the new one
        new_grid = []
        while True:
            # For each row
            for row in range(self.row_len):
                updated_row = ""
                # for each seat in each row
                for seat in range(self.col_len):
                    if self.grid[row][seat] == '.':
                        if self.debug:
                            print(f"\nDEBUG: Char: {self.grid[row][seat]}")
                        updated_row += '.'
                    else:
                        updated_row += self.step((row, seat))
                new_grid.append(updated_row)
                print(updated_row)
            
            # check to see if the grids are equal
            if self.grid == new_grid:
                break
            self.grid = new_grid
            new_grid = []
            print("-----------------------------------------------")
            

        # Combine all of the rows into a single string and count
        # the occupied seats
        print("--------------------PART 1-----------------------")
        print(f"Answer: {''.join(self.grid).count('#')}")

    def line_check(self, seat: tuple):
        """
        Determine if the seat's state should flip or stay the same.
        :param seat (tuple): place of the seat in the grid
        :return either L for unoccupied or # for occupied
        """
        is_occupied = self.grid[seat[0]][seat[1]] == '#'
        
        if self.debug:
            print(f"\nDEBUG: id: {seat}. Char: {self.grid[seat[0]][seat[1]]}")

        neighbors = 0
        
        # construct each line of sight
        line_rules = {
            "up": (-1,0),
            "upright": (-1,+1),
            "right": (0,+1),
            "downright": (+1,+1),
            "down": (+1,0),
            "downleft": (+1,-1),
            "left": (0,-1),
            "upleft": (-1,-1)
        }
        # for each direction, go until you hit an L, #, or out of range
        for direction_name, slope in line_rules.items():
            current = seat
            if self.debug:
                print(f"DEBUG: Direction: {direction_name}")
            while True:
                current = tuple(map(operator.add, current, slope))
                # if the index is out of range, then break (no new neighbor)
                if current[0] < 0 or current[0] > self.row_len-1 \
                    or current[1] < 0 or current[1] > self.col_len-1:
                    if self.debug:
                        print(f"DEBUG: {current} - Out of bounds")
                    break
                seat_in_question = self.grid[current[0]][current[1]]
                if seat_in_question == '#':
                    neighbors += 1
                    if self.debug:
                        print(f"DEBUG: Neighbor found in {direction_name} - {current}")
                    break
                elif seat_in_question == 'L':
                    if self.debug:
                        print(f"DEBUG: {current} - L")
                    break
                # else it's a . and you continue to the next seat
                if self.debug:
                        print(f"DEBUG: {current} - Floor")
            
        if self.debug:
            print(f"DEBUG: Neighbor count: {neighbors}")
        if is_occupied:
            # if neighbors > 4, return L. else return #
            if neighbors > 4:
                return 'L'
            return '#'
        else:
            # if neighbors > 1, return L. else return #
            if neighbors == 0:
                return '#'
            return 'L'


    def part_two_function(self):
        """
        Figure out the number of occupied seats after the simulation
        has settled. New rules for occupied/empty seats.
        """
        new_grid = []
        while True:
            # For each row
            for row in range(self.row_len):
                updated_row = ""
                # for each seat in each row
                for seat in range(self.col_len):
                    if self.grid[row][seat] == '.':
                        if self.debug:
                            print(f"\nDEBUG: Char: {self.grid[row][seat]}")
                        updated_row += '.'
                    else:
                        updated_row += self.line_check((row, seat))
                new_grid.append(updated_row)
                print(updated_row)
            
            # check to see if the grids are equal
            if self.grid == new_grid:
                break
            self.grid = new_grid
            new_grid = []
            print("-----------------------------------------------")
            

        # Combine all of the rows into a single string and count
        # the occupied seats
        print("--------------------PART 2-----------------------")
        print(f"Answer: {''.join(self.grid).count('#')}")



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
    seats = seating_system(input_list_path=args.input_path)
    seats.main(part_one=not args.skip_one, part_two=not args.skip_two)