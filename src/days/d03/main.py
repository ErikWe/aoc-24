import sys

sys.path.append(f'{__file__}/../../..')

from utility import try_parse_int

def solve(raw_data):
    print(f'{exceute_and_sum_all_mul_statements(raw_data, False)} | {exceute_and_sum_all_mul_statements(raw_data, True)}')

def exceute_and_sum_all_mul_statements(text, use_conditions):
    if use_conditions is False:
        text = text.replace('don\'t()', '')
    
    return exceute_and_sum_all_mul_statements_with_conditions(text)

def exceute_and_sum_all_mul_statements_with_conditions(text):
    sum = 0
    mul_enabled = True

    components = text.split('mul(')

    for i, component in enumerate(components):
        if i > 0:
            mul_enabled = determine_exiting_mul_enabled_status(components[i - 1], mul_enabled)

        if mul_enabled == False:
            continue

        text = component.split(')')[0]

        if text == components:
            continue

        sum += try_execute_inner_mul_statement(text)

    return sum

def try_execute_inner_mul_statement(text):
    components = text.split(',')

    if len(components) != 2:
        return 0
    
    a_valid, a = try_parse_int(components[0])
    b_valid, b = try_parse_int(components[1])

    if a_valid is False or b_valid is False:
        return 0
    
    if a > 999 or b > 999 or a < 0 or b < 0:
        return 0
    
    return a * b

def determine_exiting_mul_enabled_status(text, initial_status):
    last_enable = text.rfind('do()')
    last_disable = text.rfind('don\'t()')

    if last_enable > last_disable:
        return True
    
    if last_disable > last_enable:
        return False
    
    return initial_status

if __name__ == '__main__':
    from utility import parse_args_day, read_data

    args = parse_args_day(3)

    raw_data = read_data(args.inputfile)

    solve(raw_data)