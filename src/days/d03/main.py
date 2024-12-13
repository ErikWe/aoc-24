import re

def solve(raw_data):
    sum_without_conditions = exceute_and_sum_all_mul_statements(raw_data, False)
    sum_with_conditions = exceute_and_sum_all_mul_statements(raw_data, True)

    return sum_without_conditions, sum_with_conditions

def exceute_and_sum_all_mul_statements(text, use_conditions):
    return exceute_and_sum_all_mul_statements_with_conditions(text, use_conditions)

def exceute_and_sum_all_mul_statements_with_conditions(text, use_conditions):
    sum = 0
    mul_enabled = True

    for match in re.finditer(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)', text):
        if use_conditions:
            mul_enabled = determine_exiting_mul_enabled_status(text[:match.start()], mul_enabled)

        if mul_enabled == False:
            continue
        
        sum += int(match.group(1)) * int(match.group(2))

    return sum

def determine_exiting_mul_enabled_status(text, initial_status):
    match = re.search(r'(\)\(od|\)\(t\'nod)', text[::-1])

    if match is None:
        return initial_status
    
    return match.group() == ')(od'

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(3).inputfile)))