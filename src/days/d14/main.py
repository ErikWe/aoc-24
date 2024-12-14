import math
import re

class Robot:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

def solve(raw_data):
    map_size = (101, 103)

    robots = parse_robots(raw_data)

    final_robot_position = find_final_robot_positions(robots, 100, map_size)

    safety_factor = compute_safety_factor(final_robot_position, map_size)

    return safety_factor, 0

def compute_safety_factor(robot_positions, map_size):
    robots_per_quadrant = [0] * 4

    for robot_position in robot_positions:
        quadrant = find_quadrant_index(robot_position, map_size)

        if (quadrant == -1):
            continue

        robots_per_quadrant[quadrant] += 1

    return math.prod(robots_per_quadrant)

def find_final_robot_positions(robots, time, map_size):
    return [find_robot_position(robot, time, map_size) for robot in robots]

def find_robot_position(robot, time, map_size):
    absolute_final_position = (robot.position[0] + time * robot.velocity[0], robot.position[1] + time * robot.velocity[1])

    return (absolute_final_position[0] % map_size[0], absolute_final_position[1] % map_size[1])

def find_quadrant_index(position, map_size):
    vertical_divider = (map_size[0] - 1) / 2
    horizontal_divider = (map_size[1] - 1) / 2

    if position[0] == vertical_divider or position[1] == horizontal_divider:
        return -1
    
    if position[0] > vertical_divider:
        if position[1] > horizontal_divider:
            return 0
        
        return 3
    
    if position[1] > horizontal_divider:
        return 1
    
    return 2

def parse_robots(raw_data):
    return [parse_robot(robot_text) for robot_text in raw_data.splitlines()]

def parse_robot(raw_text):
    match = re.search(r'p=(-?[0-9]*),(-?[0-9]*) v=(-?[0-9]*),(-?[0-9]*)', raw_text)
    
    position = (int(match.group(1)), int(match.group(2)))
    velocity = (int(match.group(3)), int(match.group(4)))

    return Robot(position, velocity)

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(14).inputfile)))