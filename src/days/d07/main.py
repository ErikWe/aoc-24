import argparse

class Equation:
    def __init__(self, result, components):
        self.result = result
        self.components = components

def main(raw_data):
    equations = parse_equations(raw_data)

    solvable_equations_sum_without_concatenation = sum_solvable_equations_without_concatenation(equations)
    solvable_equations_sum_with_concatenation = sum_solvable_equations_with_concatenation(equations)

    report_solvable_equations_sum_without_concatenation(solvable_equations_sum_without_concatenation)
    report_solvable_equations_sum_with_concatenation(solvable_equations_sum_with_concatenation)

def report_solvable_equations_sum_without_concatenation(solvable_equations_sum):
    print(f'The sum of all solvable equations, without using concatenation, is: {solvable_equations_sum}')

def report_solvable_equations_sum_with_concatenation(solvable_equations_sum):
    print(f'The sum of all solvable equations, using concatenation, is: {solvable_equations_sum}')

def sum_solvable_equations_without_concatenation(equations):
    return sum_solvable_equations(equations, [operator_addition, operator_multiplication])

def sum_solvable_equations_with_concatenation(equations):
    return sum_solvable_equations(equations, [operator_addition, operator_multiplication, operator_concatenation])

def sum_solvable_equations(equations, operators):
    sum = 0
    
    for equation in equations:
        if can_solve_equation(equation, operators):
            sum += equation.result

    return sum

def can_solve_equation(equation, operators):
    for possible_result in get_possible_results(equation.components, operators):
        if possible_result == equation.result:
            return True

    return False

def get_possible_results(components, operators):
    if len(components) == 1:
        yield components[0]
        return
    
    for operator in operators:
        for possible_a in get_possible_results(components[:-1], operators):
            yield operator(possible_a, components[-1])

def operator_addition(a, b):
    return a + b

def operator_multiplication(a, b):
    return a * b

def operator_concatenation(a, b):
    return int(str(a) + str(b))

def parse_equations(raw_data):
    equations = []

    for equation in raw_data.split('\n'):
        result = int(equation.split(':')[0])

        components = [int(component) for component in equation.split(':')[1].split()]

        equations.append(Equation(result, components))

    return equations

def parse_args():
    parser = argparse.ArgumentParser(description='Advent of Code 2024 - Day 07')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

args = parse_args()

raw_data = open(args.inputfile, 'r', encoding='utf-8-sig').read()

main(raw_data)