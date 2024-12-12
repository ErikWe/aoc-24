class Equation:
    def __init__(self, result, components):
        self.result = result
        self.components = components

def solve(raw_data):
    equations = parse_equations(raw_data)

    print(f'{sum_solvable_equations(equations, get_simple_operator_set())} | {sum_solvable_equations(equations, get_extended_operator_set())}')

def sum_solvable_equations(equations, operators):
    return sum([equation.result for equation in equations if can_solve_equation(equation, operators)])

def can_solve_equation(equation, operators):
    return equation.result in get_possible_results(equation.components, operators)

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

def get_simple_operator_set():
    return [operator_addition, operator_multiplication]

def get_extended_operator_set():
    return [operator_addition, operator_multiplication, operator_concatenation]

def parse_equations(raw_data):
    equations = []

    for equation in raw_data.split('\n'):
        result = int(equation.split(':')[0])

        components = [int(component) for component in equation.split(':')[1].split()]

        equations.append(Equation(result, components))

    return equations

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, read_data

    args = parse_args_day(7)

    raw_data = read_data(args.inputfile)

    solve(raw_data)