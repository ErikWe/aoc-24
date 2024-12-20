import sys

sys.path.append(f'{__file__}/../../..')

from utility import Direction_2d, Directions_2d, direction_as_flag, get_next_tile, turn_clockwise

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

def solve(raw_data):
    initial_character_state, map = parse_map(raw_data)

    explored_tiles_count = explore_until_outside_map_or_loop_and_count_explored_tiles(initial_character_state, map)
    new_obstructions_resulting_in_loop_count = count_new_obstructions_resulting_in_loop(initial_character_state, map)

    return explored_tiles_count, new_obstructions_resulting_in_loop_count

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
        tile_ahead = get_next_tile(current_character_state.tile, current_character_state.direction)

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
    tile_ahead = get_next_tile(initial_character_state.tile, initial_character_state.direction)

    if is_tile_obstructed(tile_ahead, map):
        return Character_State(initial_character_state.tile, turn_clockwise(initial_character_state.direction))

    return Character_State(tile_ahead, initial_character_state.direction)

def is_loop(initial_character_state, map):
    final_character_state = explore_until_outside_map_or_loop(initial_character_state, map)[0]

    return is_tile_on_map(final_character_state.tile, map)

def count_explored_tiles(explored_character_directions_by_tile):
    return len(explored_character_directions_by_tile.keys())

def contains_character_state(character_state, character_directions_by_tile):
    if character_state.tile not in character_directions_by_tile:
        return False

    return character_directions_by_tile[character_state.tile] & direction_as_flag(character_state.direction) != Directions_2d.NONE

def is_tile_on_map(tile, map):
    return tile in map.obstructed_tiles or tile in map.unobstructed_tiles

def is_tile_outside_map(tile, map):
    return not is_tile_on_map(tile, map)

def is_tile_obstructed(tile, map):
    return tile in map.obstructed_tiles

def is_tile_unobstructed(tile, map):
    return tile in map.unobstructed_tiles

def add_explored_character_state(current_character_state, explored_character_directions_by_tile):
    if current_character_state.tile not in explored_character_directions_by_tile:
        explored_character_directions_by_tile[current_character_state.tile] = Directions_2d.NONE

    explored_character_directions_by_tile[current_character_state.tile] |= direction_as_flag(current_character_state.direction)

def parse_map(raw_data):
    obstructed_tiles = set()
    unobstructed_tiles = set()
    initial_character_state = None

    for y_coord, text_row in enumerate(raw_data.splitlines()):
        for x_coord, tile_character in enumerate(text_row):
            tile = (x_coord, y_coord)

            if tile_character == '^':
                initial_character_state = Character_State(tile, Direction_2d.NORTH)
                unobstructed_tiles.add(tile)
                continue

            if tile_character == '#':
                obstructed_tiles.add(tile)
                continue

            if tile_character == '.':
                unobstructed_tiles.add(tile)
                continue

    return initial_character_state, Map(obstructed_tiles, unobstructed_tiles)

if __name__ == '__main__':
    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(6).inputfile)))