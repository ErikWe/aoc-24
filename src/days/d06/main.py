import argparse
import enum

class Directions(enum.Flag):
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

class Tile:
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord

    def __eq__(self, other):
        if other is None:
            return False

        return self.x_coord == other.x_coord and self.y_coord == other.y_coord

    def __hash__(self):
        return hash((self.x_coord, self.y_coord))

class Character_State:
    def __init__(self, tile, direction):
        self.tile = tile
        self.direction = direction

class Map:
    def __init__(self, obstructed_tiles, unobstructed_tiles):
        self.obstructed_tiles = obstructed_tiles
        self.unobstructed_tiles = unobstructed_tiles

class Exploration:
    def __init__(self, map, current_character_state, explored_character_directions_by_tile):
        self.map = map
        self.current_character_state = current_character_state
        self.explored_character_directions_by_tile = explored_character_directions_by_tile

def main(raw_data):
    initial_character_state, map = parse_map(raw_data)

    explored_tiles_count = explore_until_outside_map_or_loop_and_count_explored_tiles(initial_character_state, map)
    new_obstructions_resulting_in_loop_count = count_new_obstructions_resulting_in_loop(initial_character_state, map)

    report_explored_tiles_count(explored_tiles_count)
    report_new_obstructions_resulting_in_loop_count(new_obstructions_resulting_in_loop_count)

def report_explored_tiles_count(explored_tiles_count):
    print(f'The number of explored tiles is: {explored_tiles_count}')

def report_new_obstructions_resulting_in_loop_count(new_obstructions_resulting_in_loop_count):
    print(f'The number of new obstructions leading to a loop is: {new_obstructions_resulting_in_loop_count}')

def explore_until_outside_map_or_loop_and_count_explored_tiles(initial_character_state, map):
    explored_character_directions_by_tile = explore_until_outside_map_or_loop(initial_character_state, map)[1]

    return count_explored_tiles(explored_character_directions_by_tile)

def explore_until_outside_map_or_loop(initial_character_state, map):
    explored_character_directions_by_tile = {}

    current_character_state = initial_character_state

    while True:
        add_explored_character_state(current_character_state, explored_character_directions_by_tile)
        
        current_character_state = explore_one_step(current_character_state, map)

        if is_tile_outside_map(current_character_state.tile, map):
            break

        if contains_character_state(current_character_state, explored_character_directions_by_tile):
            break

    return current_character_state, explored_character_directions_by_tile

def count_new_obstructions_resulting_in_loop(initial_character_state, map):
    new_obstruction_tiles = set()

    current_character_state = initial_character_state

    while is_tile_on_map(current_character_state.tile, map):
        tile_ahead = get_tile_ahead(current_character_state)

        obstructed_tiles = map.obstructed_tiles.copy()
        unobstructed_tiles = map.unobstructed_tiles.copy()

        if is_tile_on_map(tile_ahead, map) and is_tile_unobstructed(tile_ahead, map):
            obstructed_tiles.add(tile_ahead)
            unobstructed_tiles.remove(tile_ahead)

            if is_loop(initial_character_state, Map(obstructed_tiles, unobstructed_tiles)) and tile_ahead != initial_character_state.tile:
                new_obstruction_tiles.add(tile_ahead)

        current_character_state = explore_one_step(current_character_state, map)

    return len(new_obstruction_tiles)

def explore_one_step(initial_character_state, map):
    tile_ahead = get_tile_ahead(initial_character_state)

    if is_tile_obstructed(tile_ahead, map):
        return Character_State(initial_character_state.tile, turn_clockwise(initial_character_state.direction))

    return Character_State(tile_ahead, initial_character_state.direction)

def is_loop(initial_character_state, map):
    final_character_state = explore_until_outside_map_or_loop(initial_character_state, map)[0]

    return is_tile_on_map(final_character_state.tile, map)

def turn_clockwise(initial_direction):
    if initial_direction == Directions.NORTH:
        return Directions.EAST

    if initial_direction == Directions.EAST:
        return Directions.SOUTH

    if initial_direction == Directions.SOUTH:
        return Directions.WEST

    if initial_direction == Directions.WEST:
        return Directions.NORTH

def get_tile_ahead(character_state):
    return step_tile(character_state.tile, character_state.direction)

def step_tile(initial_tile, direction):
    if direction == Directions.NORTH:
        return step_tile_north(initial_tile)

    if direction == Directions.EAST:
        return step_tile_east(initial_tile)

    if direction == Directions.SOUTH:
        return step_tile_south(initial_tile)

    if direction == Directions.WEST:
        return step_tile_west(initial_tile)

def step_tile_east(initial_tile):
    return Tile(initial_tile.x_coord + 1, initial_tile.y_coord)

def step_tile_south(initial_tile):
    return Tile(initial_tile.x_coord, initial_tile.y_coord + 1)

def step_tile_west(initial_tile):
    return Tile(initial_tile.x_coord - 1, initial_tile.y_coord)

def step_tile_north(initial_tile):
    return Tile(initial_tile.x_coord, initial_tile.y_coord - 1)

def count_explored_tiles(explored_character_directions_by_tile):
    return len(explored_character_directions_by_tile.keys())

def contains_character_state(character_state, character_directions_by_tile):
    if character_state.tile not in character_directions_by_tile:
        return False

    return character_directions_by_tile[character_state.tile] & character_state.direction != Directions.NONE

def is_tile_on_map(tile, map):
    return tile in map.obstructed_tiles or tile in map.unobstructed_tiles

def is_tile_outside_map(tile, map):
    return tile not in map.obstructed_tiles and tile not in map.unobstructed_tiles

def is_tile_obstructed(tile, map):
    return tile in map.obstructed_tiles

def is_tile_unobstructed(tile, map):
    return tile in map.unobstructed_tiles

def add_explored_character_state(current_character_state, explored_character_directions_by_tile):
    if current_character_state.tile not in explored_character_directions_by_tile:
        explored_character_directions_by_tile[current_character_state.tile] = Directions.NONE

    explored_character_directions_by_tile[current_character_state.tile] |= current_character_state.direction

def parse_map(raw_data):
    obstructed_tiles = set()
    unobstructed_tiles = set()
    initial_character_state = None

    for y_coord, text_row in enumerate(raw_data.split("\n")):
        for x_coord, tile_character in enumerate(text_row):
            tile = Tile(x_coord, y_coord)

            if tile_character == '^':
                initial_character_state = Character_State(tile, Directions.NORTH)
                unobstructed_tiles.add(tile)
                continue

            if tile_character == '#':
                obstructed_tiles.add(tile)
                continue

            if tile_character == '.':
                unobstructed_tiles.add(tile)
                continue

    return initial_character_state, Map(obstructed_tiles, unobstructed_tiles)

def parse_args():
    parser = argparse.ArgumentParser(description='Advent of Code 2024 - Day 06')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

args = parse_args()

raw_data = open(args.inputfile, 'r', encoding='utf-8-sig').read()

main(raw_data)