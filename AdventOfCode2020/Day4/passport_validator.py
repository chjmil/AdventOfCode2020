import argparse
import os
import re

def passport_validator(passport: dict, ignore_cid: bool = True,
                       verify_values: bool = True):
    """
    Take the passed passport and verify if it contains the 8 required
    fields. If ignore_cid == true, then ignore that field for validation 
    purposes.
    :param passport (dict): dictionary of the passport
    :param ignore_cid (bool): if true, ignore the cid field
    :param verify_values (bool): if true, also check the values of each field (part 2)
    :return true if passport is valid
    """
    valid_template = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    if not ignore_cid:
        valid_template.append('cid')
    # Sort the keys
    valid_template.sort()
    passport_keys = list(passport.keys())
    passport_keys.sort()
    # remove the cid field
    if ignore_cid and 'cid' in passport_keys:
        passport_keys.remove('cid')
    if valid_template != passport_keys:
        # Invalid format
        print("Invalid Format")
        return False
    if not verify_values:
        return True

    # PART 2 - Value Validator
    byr = passport['byr']
    if not re.match("^19[2-9][0-9]$|^200[0-2]$", byr):
        # invalid byr
        print(f"Invalid byr: {byr}")
        return False
    
    iyr = passport['iyr']
    if not re.match("^201[0-9]$|^2020$", iyr):
        # invalid iyr
        print(f"Invalid iyr: {iyr}")
        return False
    
    eyr = passport['eyr']
    if not re.match("^202[0-9]$|^2030$", eyr):
        # invalid eyr
        print(f"Invalid eyr: {eyr}")
        return False
    
    hgt = passport['hgt']
    if 'cm' in hgt:
        if not re.match('^(1[5-8][0-9]|19[0-3])cm$', hgt):
            print(f"Invalid hgt: {hgt}")
            return False
    elif 'in' in hgt:
        if not re.match('^(59|6[0-9]|7[0-6])in$', hgt):
            print(f"Invalid hgt: {hgt}")
            return False
    else:
        print(f"Invalid hgt: {hgt}")
        return False

    hcl = passport['hcl']
    if not re.match('^#[0-9a-f]{6}$', hcl):
        print(f"Invalid hcl: {hcl}")
        return False
    
    ecl = passport['ecl']
    if not re.match('amb|blu|brn|gry|grn|hzl|oth', ecl):
        print(f"Invalid ecl: {ecl}")
        return False
    
    pid = passport['pid']
    if not re.match("^[0-9]{9}$", pid):
        print(f"Invalid pid: {pid}")
        return False

    sort = f"byr:{passport['byr']} iyr:{passport['iyr']} eyr:{passport['eyr']} hcl:{passport['hcl']} ecl:{passport['ecl']} pid:{passport['pid']} hgt:{passport['hgt']}"
    print(f"Valid Passport: {sort}")
    return True
    


def main(input_list_path: str, verify_values: bool):
    """
    Parse through the provided file for valid passports.
    :param input_list_path (str): path to the input file
    :param verify_values (bool): if true, verify the values for each field
    """
    # Verify the file exists
    if not os.path.exists(input_list_path):
        print(f"Input file does not exist: {input_list_path}")
        exit(1)

    # Parse the file and store it in a list
    with open(input_list_path, 'r') as f:
        input = f.readlines()
    
    valid_passport_count = 0
    invalid_count = 0
    current_passport = {}
    for i in input:
        # if it is an empty line, that is the end of this entry
        if i == '\n':
            if passport_validator(current_passport, verify_values=verify_values):
                valid_passport_count += 1
            else:
                invalid_count += 1
            # print(f"{invalid_count + valid_passport_count} = {valid_passport_count} + {invalid_count}")
            current_passport = {}
            continue
        # break apart the key:value pairs separated by spaces and put them in a dictionary
        current_passport.update(dict((x.strip(), y.strip()) for x,y in (element.split(':') for element in i.split(' '))))

    # get the last passport    
    if passport_validator(current_passport, verify_values=verify_values):
        valid_passport_count += 1
    else:
        invalid_count += 1
    
    # Print the solution
    print(f"Valid passports: {valid_passport_count}")
    print(f"Invalid passports: {invalid_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate the passports in the provided file.")
    parser.add_argument("--input-path", help="Path to the input file", 
                        type=str, required=True)
    parser.add_argument("--verify-values", action='store_true', help="Verify the values in addition to the fields", 
                        required=False, default=False)

    args = parser.parse_args()
    main(input_list_path=args.input_path, verify_values=args.verify_values)