class State:
    def __init__(self, a, b, c, instruction_pointer, instructions, output):
        self.a = a
        self.b = b
        self.c = c

        self.instruction_pointer = instruction_pointer
        self.instructions = instructions

        self.output = output

def solve(raw_data):
    state = parse_state(raw_data)

    execute(state)

    return str.join(',', [str(value) for value in state.output]), 0

def execute(state):
    while state.instruction_pointer < len(state.instructions):
        step(state)

def step(state):
    opcode = state.instructions[state.instruction_pointer]

    get_operation(opcode)(state)

def get_operation(opcode):
    operations = [execute_adv, execute_bxl, execute_bst, execute_jnz, execute_bxc, execute_out, execute_bdv, execute_cdv]

    return operations[opcode]

def execute_adv(state):
    state.a = eveluate_division(state)

    state.instruction_pointer += 2

def execute_bxl(state):
    state.b ^= evaluate_current_literal_operand(state)

    state.instruction_pointer += 2

def execute_bst(state):
    state.b = evaluate_current_combo_operand(state) % 8

    state.instruction_pointer += 2

def execute_jnz(state):
    if state.a == 0:
        state.instruction_pointer += 2
    
    if state.a > 0:
        state.instruction_pointer = evaluate_current_literal_operand(state)

def execute_bxc(state):
    state.b ^= state.c

    state.instruction_pointer += 2

def execute_out(state):
    state.output.append(evaluate_current_combo_operand(state) % 8)

    state.instruction_pointer += 2

def execute_bdv(state):
    state.b = eveluate_division(state)

    state.instruction_pointer += 2

def execute_cdv(state):
    state.c = eveluate_division(state)

    state.instruction_pointer += 2

def eveluate_division(state):
    numerator = state.a
    denominator = 2 ** evaluate_current_combo_operand(state)

    return numerator // denominator

def evaluate_current_literal_operand(state):
    return state.instructions[state.instruction_pointer + 1]

def evaluate_current_combo_operand(state):
    return evaluate_combo_operand(state.instructions[state.instruction_pointer + 1], state)

def evaluate_combo_operand(combo_operand, state):
    if combo_operand <= 3:
        return combo_operand
    
    if combo_operand == 4:
        return state.a
    
    if combo_operand == 5:
        return state.b
    
    if combo_operand == 6:
        return state.c

def parse_state(raw_data):
    lines = raw_data.splitlines()

    a = int(lines[0].split()[2])
    b = int(lines[1].split()[2])
    c = int(lines[2].split()[2])

    program = [int(x) for x in lines[4].split()[1].split(',')]

    return State(a, b, c, 0, program, [])

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')
    
    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(17).inputfile)))