import argparse
import os
from copy import deepcopy

# An attempt at using a linked list to figure this out. It works on small
# inputs but hits a recursion error on large inputs. So sad :'(
# region linked_list
class line_obj:
    """
    Linked list object to make it easy to work backwards
    """
    def __init__(self,
                 instruct: tuple,
                 line_number: int,
                 has_replaced: bool):
        self.instruct = instruct
        self.line_number = line_number
        self.has_replaced = has_replaced
        global head
        global root
        if root is None:
            root = head = self
            self.has_replaced = False
            self.__parent = None
        else:
            head.append(self)
    
    def __str__(self):
        return f"Instruction: {self.instruct}\n"\
               f"Line Number: {self.line_number}\n"\
               f"Has_replaced: {self.has_replaced}\n"\
               f"parent: {self.parent}"

    # region Getters and Setters
    @property
    def parent(self):
        return self.__parent
    @parent.setter
    def parent(self, parent):
        self.__parent = parent
    # endregion
    
    def find_replaced(self):
        """
        Recursively find the first value where has_replaced = False
        Delete nodes as they go
        """
        if not self.has_replaced:
            return self
        return self.parent.find_replaced()
    
    def append(self, node):
        """
        Set this node as the parent and update the has_replaced value
        """
        global head
        node.parent = self
        head = node
    
    def rollback(self):
        """
        Roll back to the initial replaced jmp
        """
        global visited_lines_list
        global accumulator
        global logs
        logs.pop()
        visited_lines_list.pop()
        if self.has_replaced:
            if self.instruct[0] == 'acc':
                print(f"Removing: {self.instruct[1]}")
                accumulator -= self.instruct[1]
            return self.parent.rollback()
        else:
            self.has_replaced = False
            return self

# Head of the linked list
root: line_obj = None
head: line_obj = None
accumulator: int = 0
visited_lines_list = []
bad_jmps = set()
logs = []

def linked_list_traverser(input: str, line_number: int, replaced: bool):
    """
    Construct a linked list to hold all of the instructions.
    Execute each line until we hit an infinite loop. Try replacing the jump.
    If we hit another infinite loop, go back up to the replaced instruction and 
    revert it.
    :param input (str): next line to execute
    :param line_number (int): current line number to execute
    :return the accumulator value
    """
    if line_number == len(input):
        print("Program terminated successfully.")
        return 0
    line = input[line_number]
    instruction = line.split(' ')
    accum = int(instruction[1])
    instruction = (instruction[0], accum)
    logs.append(instruction)

    visited_lines_list.append(line_number)
    # If it is in the list more than onces, it's in a loop
    if len([i for i,x in enumerate(visited_lines_list) if x == line_number]) > 1:
        print("Detecting infinite loop. Rolling back...")
        global head
        new_head = head.rollback()
        head = new_head
        print(f"Rolled back to {head.instruct}")
        bad_jmps.add(new_head.line_number)
        visited_lines_list.pop()
        return linked_list_traverser(input, new_head.line_number, replaced=False)
    
    # Create a new node for this set of instructions
    line_obj(instruct=instruction, line_number=line_number, has_replaced=replaced)
    print(line.strip())

    if instruction[0] == 'acc':
        print(f"Adding: {accum}")
        return linked_list_traverser(input, line_number+1, replaced=replaced) + accum
    elif instruction[0] == 'jmp':
        if replaced or line_number in bad_jmps:
            return linked_list_traverser(input, line_number+accum, replaced=replaced)
        else:
            # replace it with nop
            print(f"Replacing {input[line_number].strip()} with nop")
            logs.pop()
            logs.append("NOP")
            return linked_list_traverser(input, line_number+1, replaced=True)
    else:
        return linked_list_traverser(input, line_number+1, replaced=replaced)
# endregion


class InfiniteLoopException(Exception):
    """
    Exception raised when the input leads to an infinite loop
    """

visited_lines = set()
def next_line(input: str, line_number: int, raise_exception: bool = False):
    """
    Recursively execute the next line.
    :param input (str): next line to execute
    :param line_number (int): current line number to execute
    :param raise_exception (bool): if true, raise an exception on infinite loop
    :return the accumulator value
    """
    if line_number == len(input):
        print("Program terminated successfully.")
        return 0
    line = input[line_number]
    instruction, accum = line.split(' ')
    accum = int(accum)

    current_len = len(visited_lines)
    visited_lines.add(line_number)
    if current_len == len(visited_lines):
        print("Detecting infinite loop. Exiting...")
        if raise_exception:
            raise InfiniteLoopException
        return 0
    
    print(line.strip())

    if instruction == 'acc':
        return next_line(input, line_number+1, raise_exception=raise_exception) + accum
    elif instruction == 'jmp':
        return next_line(input, line_number+accum, raise_exception=raise_exception)
    else:
        return next_line(input, line_number+1, raise_exception=raise_exception)

def last_acc_value(input: list):
    """
    Find the final value of the accumulator before it begins the 
    infinite loop.
    :param input (list): list of instructions to read through
    """
    accumulator = 0
    accumulator = next_line(input, 0)

    # Print the solution
    print("--------------------PART 1-----------------------")
    print(f"Answer: {accumulator}")

def jmp_replacer(input: list):
    """
    Replace a single jmp with nop and see if the program terminates
    :param input (list): list of instructions to read through
    :return accumulator total after a clean termination
    """
    # list of line numbers where the line is a jmp
    jmp_list = []
    for i in range(len(input)):
        if 'jmp' in input[i]:
            jmp_list.append(i)
    
    for attempt in jmp_list:
        try:
            # clear out the lists
            global visited_lines
            visited_lines = set()
            new_input = deepcopy(input)
            new_input[attempt] = 'nop +0'
            total = next_line(new_input, 0, raise_exception=True)
            return total
        except InfiniteLoopException as e:
            print(f"Replacing line {attempt} did not work.\n\n")

def replace_loop(input: list):
    """
    Replace one jmp with a nop to break the infinite loop.
    :param input (list): list of instructions to read through
    """
    
    accumulator = jmp_replacer(input)
    # Print the solution
    print("--------------------PART 2-----------------------")
    print(logs)
    print(f"Answer: {accumulator}")



def main(input_list_path: str, part_one: bool):
    """
    Parse through the provided file for the list of instructions
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

    if part_one:
        last_acc_value(input)
    else:
        replace_loop(input)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the program.")
    parser.add_argument("--input-path", help="Path to the input file", 
                        type=str, required=True)
    parser.add_argument("--part1", help="Run the program in respect to part 1", 
                        action="store_true", dest="part_one")
    parser.add_argument("--part2", help="Run the program in respect to part 2", 
                        action="store_false", dest="part_one")

    args = parser.parse_args()
    main(input_list_path=args.input_path, part_one=args.part_one)