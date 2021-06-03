"""
Template file to make it easier to copy the basic structure.
"""
import argparse
import os
import re

# global dict to hold all of the bags and their children
bag_rules: dict = {}
parents: list = []

def get_possible_parents(bag_color: str):
    """
    Get all of the bags that contain the bag_color
    :param bag_color (str): color of the bag to search for
    :return number of possible parents
    """
    color_list = []
    color_regex = re.compile(f'\d+ {bag_color}')
    for key in bag_rules:
        for child in bag_rules[key]:
            if color_regex.match(child):
                color_list.append(key)
                print(f"Parent: {key}, Children: {bag_rules[key]}")
                continue
    # Recursively get all of the parents
    for color in color_list:
        if color not in parents:
            get_possible_parents(color)
    
    parents.extend(color_list)
    
    return color_list

def part_one_func(bag_color: str):
    """
    Run through part 1 of the problem
    :param bag_color (str): color of the bag to search for
    """
    get_possible_parents(bag_color=bag_color)

    print(f"Set of unique colors: {set(parents)}")    
    # Print the solution
    print("--------------------PART 1-----------------------")
    print(f"Answer: {len(set(parents))}")

def get_number_of_bags(bag_color: str):
    """
    Get the number of bags that are inside of the bag_color
    :param bag_color (str): color of the bag to search for
    :return number of bags
    """
    # get all of the child bags of the bag_color and store their innards
    innards = bag_rules[bag_color]
    total = 1
    number_regex = re.compile('(\d+) ([^.]*)\.?$')
    print(f'{bag_color}: {innards}')
    for bag in innards:
        if 'no other' in bag:
            return 1
        match = number_regex.match(bag)
        number = int(match[1])
        color = match[2]
        inside = get_number_of_bags(color)
        total += number * inside
    return total

def part_two_func(bag_color: str):
    """
    Run through part 2 of the problem
    :param bag_color (str): color of the bag to search for
    """
    total = get_number_of_bags(bag_color)

    # Print the solution
    print("--------------------PART 2-----------------------")
    print(f"Answer: {total-1}")


    

def main(input_list_path: str, bag_color: str, part_one: bool = False):
    """
    Parse through the provided file for bags and their child bags. Figure
    out how many bags could possibly contain a specific one.
    :param input_list_path (str): Path to the input file
    :param bag_color (str): Color of the bag to search for
    """
    # Verify the file exists
    if not os.path.exists(input_list_path):
        print(f"Input file does not exist: {input_list_path}")
        exit(1)

    # Parse the file and store it in a list
    with open(input_list_path, 'r') as f:
        # List comprehension to read in all of the rules
        input = [x.split('contain') for x in f.readlines()]
    
    # break up the rules and put them in the global dict
    bag_remover = re.compile(' bag(s)?')
    for rule in input:
        parent, child = rule
        child = bag_remover.sub('', child)
        child = [c.strip() for c in child.split(',')]
        parent = bag_remover.sub('', parent)
        bag_rules[parent.strip()] = child
    
    if part_one:
        part_one_func(bag_color)
        exit(0)
    
    part_two_func(bag_color)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the program.")
    parser.add_argument("--input-path", help="Path to the input file", 
                        type=str, required=True)
    parser.add_argument("--color", help="Color of the bag", 
                        type=str, required=True)
    parser.add_argument("--part2", help="Select if you want to run part 2", 
                        action='store_true')

    args = parser.parse_args()
    main(input_list_path=args.input_path, bag_color=args.color, part_one=not args.part2)