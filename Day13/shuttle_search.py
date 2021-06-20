import argparse
import os

class shuttle_search():

    def __init__(self, input_list_path: str):
        """
        Handle the input file and store the contents in a class variable
        :param input_list_path (str): Path to the input file
        """
        self.wait_time = 0
        self.buses = []
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
            self.wait_time = int(f.readline())
            self.buses = f.readline().split(',')

    def part_one_function(self):
        """
        Figure out which bus will make us wait the least amount of time
        """
        # remove the x's
        self.buses = [x for x in self.buses if x != 'x']
        self.buses = [int(x) for x in self.buses]
        min_time = int(self.buses[0])-1
        min_bus = None
        for bus in self.buses:
            current_time = bus - self.wait_time % bus
            # if current_time == bus, that means it arrives at the same time
            if current_time == bus: current_time = 0
            if current_time < min_time:
                min_time = current_time
                min_bus = bus
        
        # Print the solution
        print("--------------------PART 1-----------------------")
        print(f"Answer: {min_bus * min_time}")


    def slow_part_two_function(self):
        """
        Method is fine for small sets, but can't handle large ones. So sad :(
        Find the earliest timestamp such that all of the listed bus IDs
        depart at offsets matching their positions in the list 
        """
        timestamp = 0
        iteration = 0
        order = {}
        for bus in self.buses:
            if bus == 'x':
                iteration += 1
                continue
            order[iteration] = int(bus)
            iteration += 1
        
        iteration = 1
        while True:
            if self.debug:
                print(f"\nIteration {iteration} - Timestamp: {iteration*order[0]}")
            # Get a timestamp where the first bus is just leaving
            timestamp = iteration * order[0]
                    
            # increment this variable for each other bus. If something
            # is out of order, then the timestamp isn't good
            current_times = []
            for delay, bus in order.items():
                bus_time = bus - (timestamp) % bus
                if bus_time == bus: bus_time = 0
                if bus_time in current_times:
                    # Can't already be in the list
                    break
                if len(current_times) > 0 and current_times[-1] > bus_time:
                    # bus time can't be greater than the previous time
                    break
                if bus_time > order[0]:
                    # if bus_time is too large, bus 1 will arrive before it
                    break
                current_times.append(bus_time)
            if self.debug:
                print(f"Current list: {current_times}")

            if len(current_times) == len(order) and \
                current_times == list(order.keys()):
                break
            iteration +=1

        # Print the solution
        print("--------------------PART 2-----------------------")
        print(f"Answer: {timestamp}")

    def fast_part_two_function(self):
        """
        Use Chinese Remainder Theorem to figure out the timestamp.
        This works because all of the bus numbers are prime
        https://en.wikipedia.org/wiki/Chinese_remainder_theorem
        """
        order = {}
        for i, bus in enumerate(self.buses):
            if bus == 'x':
                continue
            order[int(bus)] = -i % int(bus)
        
        iteration = 0
        increment = 1
        for bus in order.keys():
            while iteration % bus != order[bus]:
                iteration += increment
            increment *= bus

        # Print the solution
        print("--------------------PART 2-----------------------")
        print(f"Answer: {iteration}")


    def peek(self, start):
        """
        Create a file that lists which buses are leaving 
        at which timestamp. Shows the list from the first bus
        departure to it's second departure.
        """
        order = {}
        iteration = 0
        for bus in self.buses:
            if bus == 'x':
                iteration += 1
                continue
            order[iteration] = int(bus)
            iteration += 1

        # open a file and write every line
        bus_depart_list = []
        for i in range(order[0]+1):
            timestamp = i + start
            bus_depart_str = f"\n{timestamp:<11}"
            for delay, bus in order.items():
                is_depart = timestamp % bus == 0
                bus_depart_str += f"{'D' if is_depart else '.':<7}"
            bus_depart_list.append(bus_depart_str)
        
        with open("output.log", 'w+') as f:
            f.write(f"time     {''.join([f'bus {order[x]:<4}' for x in order.keys()])}")
            f.writelines(bus_depart_list)



    def main(self, part_one: bool = True, part_two: bool = True, peek: int = -1):
        """
        Run part one, part two, or both and output the answers.
        """
        if part_one:
            self.part_one_function()
        
        if part_two:
            self.fast_part_two_function()
        
        if peek > 0:
            self.peek(peek)
        

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
    parser.add_argument("--peek", help="Create an output file containing a peek at the values", 
                        type=int, required=False, default=-1)

    args = parser.parse_args()
    if args.debug:
        os.environ['debug'] = "True"
    shuttle = shuttle_search(input_list_path=args.input_path)
    shuttle.main(part_one=not args.skip_one, part_two=not args.skip_two, peek=args.peek)