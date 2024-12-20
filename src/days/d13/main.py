import numpy as np
import re

class Machine:
    def __init__(self, prize_position, button_a_delta, button_b_delta):
        self.prize_position = prize_position
        self.button_a_delta = button_a_delta
        self.button_b_delta = button_b_delta

def solve(raw_data):
    machines = parse_machines(raw_data)

    total_price_without_offset = compute_total_price(machines, 0)
    total_price_with_offset = compute_total_price(machines, 10000000000000)

    return total_price_without_offset, total_price_with_offset

def compute_total_price(machines, prize_position_offset):
    return sum([price for price in [compute_price_for_machine(machine, prize_position_offset) for machine in machines] if price >= 0])

def compute_price_for_machine(machine, prize_position_offset):
    prize_position = np.array(machine.prize_position) + prize_position_offset

    A = np.stack([np.stack(machine.button_a_delta), -np.stack(machine.button_b_delta)], axis=1)
    
    presses = [round(abs(x)) for x in np.linalg.solve(A, prize_position)]

    final_position = np.matmul(np.stack([np.stack(machine.button_a_delta), np.stack(machine.button_b_delta)], axis=1), presses)

    if not np.array_equal(final_position, prize_position):
        return -1

    return 3 * presses[0] + presses[1]

def parse_machines(raw_data):
    return [parse_machine(machine_text) for machine_text in raw_data.split('\n\n')]

def parse_machine(machine_text):
    lines = machine_text.splitlines()

    button_a_delta = parse_button_delta(lines[0])
    button_b_delta = parse_button_delta(lines[1])
    prize_position = parse_prize_position(lines[2])

    return Machine(prize_position, button_a_delta, button_b_delta)

def parse_button_delta(text):
    match = re.search(r'X\+([0-9]*), Y\+([0-9]*)', text)

    return (int(match.group(1))), int(match.group(2))

def parse_prize_position(text):
    match = re.search(r'X=([0-9]*), Y=([0-9]*)', text)

    return int(match.group(1)), int(match.group(2))

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(13).inputfile)))