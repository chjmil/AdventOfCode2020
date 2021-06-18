import argparse
import os

class seating_system():

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
            # Store the lines of input into the self.grid var
            self.grid = [x.strip() for x in f.readlines()]
        # Number of rows
        self.row_len = len(self.grid)
        # Number of seats (columns)
        self.col_len = len(self.grid[0])
    
    def step(self, id: tuple):
        """
        Simulate the next round to see if the seat
        changes or stays the same.
        :param id (tuple): (x, y) coordinate
        """
        x_range = [max(id[0]-1, 0), min(id[0]+1, self.col_len-2)]
        y_range = [max(id[1]-1, 0), min(id[1]+1, self.row_len-2)+1]
        # print(f"x{x_range} and y{y_range}: {self.grid[id[1]][id[0]]}")
        is_occupied = self.grid[id[1]][id[0]] == '#'

        # Wacky way to count the number of neighbors
        neighbors = ""
        for row in range(*y_range):
            neighbors += self.grid[row][x_range[0]:x_range[1]+1]
        num_neighbors = neighbors.count('#')
        if is_occupied:
            # if neighbors > 3, return L. else return #
            # subtract 1 since the seat in question is occupied
            if num_neighbors -1 > 3:
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
                        updated_row += '.'
                    else:
                        updated_row += self.step((seat, row))
                new_grid.append(updated_row)
                print(updated_row)
            
            # check to see if the grids are equal
            if self.grid == new_grid:
                break
            self.grid = new_grid
            new_grid = []
            print("---------------------")
            

        # Combine all of the rows into a single string and count
        # the occupied seats
        print("--------------------PART 1-----------------------")
        print(f"Answer: {''.join(self.grid).count('#')}")


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
    seats = seating_system(input_list_path=args.input_path)
    seats.main(part_one=not args.skip_one, part_two=not args.skip_two)