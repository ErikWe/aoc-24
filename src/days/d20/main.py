import sys

sys.path.append(f'{__file__}/../../..')

from utility import get_neighbour_tiles

class Map:
    def __init__(self, width, height, start_tile, end_tile, wall_tiles):
        self.width = width
        self.height = height
        
        self.start_tile = start_tile
        self.end_tile = end_tile
        self.wall_tiles = wall_tiles

class Cheat:
    def __init__(self, start_tile, end_tile):
        self.start_tile = start_tile
        self.end_tile = end_tile

def solve(raw_data):
    map = parse_map(raw_data)

    distances_to_end = find_distances_to_end(map)

    old_rule_cheats = find_all_cheats(2, distances_to_end, map)
    new_rule_cheats = find_all_cheats(20, distances_to_end, map)

    old_rule_cheats_saving_at_least_100_picoseconds_count = count_cheats_saving_at_least_n_picoseconds(old_rule_cheats, 100, distances_to_end)
    new_rule_cheats_saving_at_least_100_picoseconds_count = count_cheats_saving_at_least_n_picoseconds(new_rule_cheats, 100, distances_to_end)

    return old_rule_cheats_saving_at_least_100_picoseconds_count, new_rule_cheats_saving_at_least_100_picoseconds_count

def count_cheats_saving_at_least_n_picoseconds(cheats, n, distances_to_end):
    return len([cheat for cheat in cheats if get_time_saved_for_cheat(cheat, distances_to_end) >= n])

def get_time_saved_for_cheat(cheat, distances_to_end):
    return distances_to_end[cheat.start_tile] - distances_to_end[cheat.end_tile] - abs(cheat.start_tile[0] - cheat.end_tile[0]) - abs(cheat.start_tile[1] - cheat.end_tile[1])

def find_all_cheats(cheat_time, distances_to_end, map):
    return [cheat for tile in distances_to_end.keys() for cheat in find_cheats(tile, cheat_time, map)]

def find_cheats(current_tile, remaining_cheat_time, map):
    return [Cheat(current_tile, end_tile) for end_tile in find_cheat_end_tiles(current_tile, remaining_cheat_time, map)]

def find_cheat_end_tiles(cheat_start_tile, cheat_time, map):
    cheat_end_tiles = []

    for y_coord_delta in range(-cheat_time, cheat_time + 1):
        for x_coord_delta in range(-cheat_time + abs(y_coord_delta), cheat_time + 1 - abs(y_coord_delta)):
            cheat_end_tile = (cheat_start_tile[0] + x_coord_delta, cheat_start_tile[1] + y_coord_delta)

            if is_tile_outside_map(cheat_end_tile, map) or cheat_end_tile in map.wall_tiles:
                continue

            if cheat_end_tile not in map.wall_tiles:
                cheat_end_tiles.append(cheat_end_tile)

    return cheat_end_tiles

def is_tile_on_map(tile, map):
    return 0 <= tile[0] < map.width and 0 <= tile[1] < map.height

def is_tile_outside_map(tile, map):
    return not is_tile_on_map(tile, map)

def find_distances_to_end(map):
    open = [map.end_tile]
    g_scores = {}

    g_scores[map.end_tile] = 0

    while len(open) > 0:
        current_tile = open.pop()

        for neighbour_tile in get_neighbour_tiles(current_tile):
            if neighbour_tile in map.wall_tiles:
                continue

            tentative_g = g_scores[current_tile] + 1

            if neighbour_tile not in g_scores or tentative_g <= g_scores[neighbour_tile]:
                g_scores[neighbour_tile] = tentative_g

                if neighbour_tile not in open:
                    open.append(neighbour_tile)

    return g_scores

def parse_map(raw_data):
    start_tile = None
    end_tile = None
    wall_positions = set()

    for y_coord, line in enumerate(raw_data.splitlines()):
        for x_coord, content in enumerate(line):
            tile = (x_coord, y_coord)

            if content == 'S':
                start_tile = tile

            if content == 'E':
                end_tile = tile

            if content == '#':
                wall_positions.add(tile)

    width = max([wall_position[0] for wall_position in wall_positions]) + 1
    height = max([wall_position[1] for wall_position in wall_positions]) + 1

    return Map(width, height, start_tile, end_tile, wall_positions)

if __name__ == '__main__':
    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(20).inputfile)))