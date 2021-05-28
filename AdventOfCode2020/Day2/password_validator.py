import argparse
import os
import re

def password_validator_part1(rule, value):
    """
    Check to see if the value follows the rule. If so, return them.
    :param rule (str): The rule that the value must follow
    :param value (str): The password in question
    :return (rule, value) if the password is valid, else None
    """
    # break up the rule into its components
    number_range, c = rule.split(' ')
    number_range = number_range.replace('-', ',')
    validation_regex = re.compile(f"^(?:[^{c}]*{c}){{{number_range}}}[^{c}]*$")

    return validation_regex.match(value) is not None

def password_validator_part2(rule, value):
    """
    Check to see if the value follows the rule. If so, return them.
    :param rule (str): The rule that the value must follow
    :param value (str): The password in question
    :return (rule, value) if the password is valid, else None

    """
    # break up the rule into its components
    number_range, c = rule.split(' ')
    small, big = number_range.split('-')

    # check to see if the expected character is at the specified location(s)
    small_check = c == value[int(small)-1]
    big_check = c == value[int(big)-1]

    return True and (small_check ^ big_check)


def main(input_list_path: str):
    """
    Parse through the provided file for passwords and determine if they are valid
    :param input_list_path (str): 
    """
    # Verify the file exists
    if not os.path.exists(input_list_path):
        print(f"Input file does not exist: {input_list_path}")
        exit(1)

    # Parse the file and store it in a list
    with open(input_list_path, 'r') as f:
        # List comprehension to break lines into lists containing the rule and the value. 
        # also remove the \n
        input = [x.replace('\n', '').split(': ') for x in f.readlines()]
    
    # List comprehension to store all valid passwords
    valid_passwords = []
    for combo in input:
        valid_passwords.append(combo) if password_validator_part1(*combo) else None
    
    # Print the valid passwords and corresponding rules
    print("--------------------PART 1-----------------------")
    print(f"Valid passwords: {valid_passwords}")
    print(f"Number of Valid Passwords: {len(valid_passwords)}")

    valid_passwords = []
    for combo in input:
        valid_passwords.append(combo) if password_validator_part2(*combo) else None

    # Print the valid passwords and corresponding rules
    print("--------------------PART 2-----------------------")
    print(f"Valid passwords: {valid_passwords}")
    print(f"Number of Valid Passwords: {len(valid_passwords)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process the expense report.")
    parser.add_argument("--input-path", help="Path to the expense report values", 
                        type=str, required=True)

    args = parser.parse_args()
    main(input_list_path=args.input_path)