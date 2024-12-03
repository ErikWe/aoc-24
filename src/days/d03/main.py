import argparse
import enum
import sys

sys.path.append("../..")

from utility import try_parse_int

class Mul_enabled_status(enum.Enum):
    ENABLED = 1
    DISABLED = 2

def main(text):
    unconditional_result = interpret_and_sum_mul_statements(text, False)
    conditional_result = interpret_and_sum_mul_statements(text, True)

    report_unconditional_result(unconditional_result)
    report_conditional_result(conditional_result)

def report_unconditional_result(result):
    print(f'Without conditions, the sum is: {result}')
    
def report_conditional_result(result):
    print(f'With conditions, the sum is: {result}')

def interpret_and_sum_mul_statements(text, use_conditions):
    mul_statements = interpret_all_mul_statements_with_or_without_conditions(text, use_conditions)

    return execute_and_sum_mul_statements(mul_statements)

def interpret_all_mul_statements_with_or_without_conditions(text, use_conditions):
    if use_conditions:
        return interpret_all_mul_statements(text)
    
    return interpret_all_mul_statements(text.replace('don\'t()', ''))

def interpret_all_mul_statements(text):
    components = text.split('mul(')

    mul_statements = []

    mul_enabled_status = Mul_enabled_status.ENABLED

    for i, component in enumerate(components):
        if i > 0:
            mul_enabled_status = determine_exiting_mul_enabled_status(components[i - 1], mul_enabled_status)

        if mul_enabled_status == Mul_enabled_status.DISABLED:
            continue

        text = component.split(')')[0]

        if text == components:
            continue

        is_valid, a, b = try_interpret_inner_mul_statement(text)

        if is_valid:
            mul_statements.append([a, b])

    return mul_statements

def try_interpret_inner_mul_statement(text):
    components = text.split(',')

    if len(components) != 2:
        return False, None, None
    
    a_valid, a = try_parse_int(components[0])
    b_valid, b = try_parse_int(components[1])

    if a_valid is False or b_valid is False:
        return False, None, None
    
    if a > 999 or b > 999 or a < 0 or b < 0:
        pass
    
    return True, a, b

def determine_exiting_mul_enabled_status(text, initial_status):
    last_enable = text.rfind('do()')
    last_disable = text.rfind('don\'t()')

    if last_enable > last_disable:
        return Mul_enabled_status.ENABLED
    
    if last_disable > last_enable:
        return Mul_enabled_status.DISABLED
    
    return initial_status

def execute_and_sum_mul_statements(mul_statements):
    return sum_executed_mul_statements(execute_mul_statements(mul_statements))

def execute_mul_statements(mul_statements):
    return [a * b for [a, b] in mul_statements]

def sum_executed_mul_statements(executed_mul_statments):
    return sum(executed_mul_statments)

def parse_args():
    parser = argparse.ArgumentParser(description='Advent of Code 2024 - Day 03')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

args = parse_args()

text = open(args.inputfile, 'r').read()

main(text)