import argparse
import os
import re

def get_seat_id(input: str):
    """
    String contains F, B, R, and L. Convert it to a binary and then to decimal
    F means it is the lower half, B means it is the upper half
    R means upper half, L means lower half
    """
    binary_input = re.sub('F|L', '0', input)
    binary_input = re.sub('B|R', '1', binary_input)

    row = int(binary_input[:-3], base=2)
    column = int(binary_input[-3:], base=2)


    seat = row * 8 + column
    print(f"{input} = Row {row} Column {column}, seat {seat}")
    return seat


def main(input_list_path: str):
    """
    Parse through the provided file for the seat IDs
    :param input_list_path (str): Path to the input file
    """
    # Verify the file exists
    if not os.path.exists(input_list_path):
        print(f"Input file does not exist: {input_list_path}")
        exit(1)

    # Parse the file and store it in a list
    with open(input_list_path, 'r') as f:
        # List comprehension to ...
        input = f.readlines()

    largest_id = 0
    seat_list = []
    for i in input:
        seat_id = get_seat_id(i.strip())
        seat_list.append(seat_id)
        largest_id = max(largest_id, seat_id)

    # Print the solution
    print("--------------------PART 1-----------------------")
    print(f"Answer: {largest_id}")

    # PART 2
    my_seat = 0
    seat_list.sort()
    # Go through the sorted list and figure out which seat is missing
    for i in range(len(seat_list)-2):
        # Skip the first value since we are told that can't be the answer
        if i == 0:
            continue
        # if the value's +1/-1 neighbor is there, then that means it can't be our seat
        if seat_list[i]+1 == seat_list[i+1] and seat_list[i]-1 == seat_list[i-1]:
            continue
        # if we found the missing spot, then that means it is the next seat after seat_list[i]
        my_seat = seat_list[i] + 1
        break
    
    print("--------------------PART 2-----------------------")
    print(f"Answer: {my_seat}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the program.")
    parser.add_argument("--input-path", help="Path to the input file", 
                        type=str, required=True)

    args = parser.parse_args()
    main(input_list_path=args.input_path)