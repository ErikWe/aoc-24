import argparse
import enum
import functools

class Direction_2d(enum.Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

class Directions_2d(enum.Flag):
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

def direction_as_flag(direction):
    if direction == Direction_2d.NORTH:
        return Directions_2d.NORTH
    if direction == Direction_2d.EAST:
        return Directions_2d.EAST
    if direction == Direction_2d.SOUTH:
        return Directions_2d.SOUTH
    if direction == Direction_2d.WEST:
        return Directions_2d.WEST

def turn_clockwise(initial_direction):
    if initial_direction == Direction_2d.NORTH:
        return Direction_2d.EAST

    if initial_direction == Direction_2d.EAST:
        return Direction_2d.SOUTH

    if initial_direction == Direction_2d.SOUTH:
        return Direction_2d.WEST

    if initial_direction == Direction_2d.WEST:
        return Direction_2d.NORTH
    
def turn_around(initial_direction):
    return turn_clockwise(turn_clockwise(initial_direction))

def turn_counter_clockwise(initial_direction):
    return turn_around(turn_clockwise(initial_direction))

def get_next_tile(initial_position, direction):
    if direction == Direction_2d.NORTH:
        return (initial_position[0], initial_position[1] - 1)
    
    if direction == Direction_2d.EAST:
        return (initial_position[0] + 1, initial_position[1])
    
    if direction == Direction_2d.SOUTH:
        return (initial_position[0], initial_position[1] + 1)
    
    if direction == Direction_2d.WEST:
        return (initial_position[0] - 1, initial_position[1])
    
def get_neighbour_tiles(tile):
    return [get_next_tile(tile, direction) for direction in get_directions()]

def get_neighbour_tiles_with_direction(tile):
    return [(get_next_tile(tile, direction), direction) for direction in get_directions()]

def get_directions():
    return [Direction_2d.NORTH, Direction_2d.EAST, Direction_2d.SOUTH, Direction_2d.WEST]

def count_items_with_filter(list, filter):
    return functools.reduce(lambda sum, value: sum + (1 if filter(value) else 0), list, 0)

def try_parse_int(source):
    if not source.isdigit():
        return False, None

    try:
        return True, int(source)
    except ValueError:
        return False, None

def parse_args_day(day):
    parser = argparse.ArgumentParser(description=f'Advent of Code 2024 - Day {day:02d}')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

def read_data(inputfile):
    return open(inputfile, 'r', encoding='utf-8-sig').read()

def print_results(results):
    print(f'{results[0]} | {results[1]}')