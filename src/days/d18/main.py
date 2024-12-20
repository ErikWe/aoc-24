import bisect
import functools
import sys

sys.path.append(f'{__file__}/../../..')

from utility import get_neighbour_tiles

class Map:
    def __init__(self, size, corrupted_tiles):
        self.size = size
        self.corrupted_tiles = corrupted_tiles

def solve(raw_data):
    bytes = parse_bytes(raw_data)

    shortest_path_length_after_kilobyte = find_shortest_path_length_after_n_bytes(bytes, 1024, 71) - 1
    time_until_blocked = find_time_until_blocked(bytes, 71)

    return shortest_path_length_after_kilobyte, f'{bytes[time_until_blocked - 1][0]},{bytes[time_until_blocked - 1][1]}'

def find_time_until_blocked(bytes, map_size):
    start_tile = (0, 0)
    end_tile = (map_size - 1, map_size - 1)

    corrupted_tiles = []

    path = find_shortest_path(start_tile, end_tile, Map(map_size, corrupted_tiles), manhattan_distance_heuristic)

    if path is None:
        return 0
    
    path_tile_indices = {k: v for v, k in enumerate(path)}

    while True:
        new_corrupted_tile = bytes[len(corrupted_tiles)]

        corrupted_tiles.append(new_corrupted_tile)

        if new_corrupted_tile in path_tile_indices:
            corrupted_tile_index = path_tile_indices[new_corrupted_tile]

            intermediate_path = find_shortest_path(path[corrupted_tile_index - 1], path[corrupted_tile_index + 1], Map(map_size, corrupted_tiles), manhattan_distance_heuristic)

            if intermediate_path is not None:
                path = path[:corrupted_tile_index - 1] + intermediate_path + path[corrupted_tile_index + 2:]

            if intermediate_path is None:
                path = find_shortest_path(start_tile, end_tile, Map(map_size, corrupted_tiles), manhattan_distance_heuristic)

            if path is None:
                break

            path_tile_indices = {k: v for v, k in enumerate(path)}

    return len(corrupted_tiles)

def find_shortest_path_length_after_n_bytes(bytes, n_bytes, map_size):
    corrupted_tiles = simulate_program(bytes, n_bytes)

    map = Map(map_size, corrupted_tiles)

    return len(find_shortest_path((0, 0), (map.size - 1, map.size - 1), map, manhattan_distance_heuristic))

def simulate_program(bytes, time):
    corrupted_tiles = []

    for elapsed_time, byte in enumerate(bytes):
        if elapsed_time == time:
            break
        
        corrupted_tiles.append((byte[0], byte[1]))

    return corrupted_tiles

def find_shortest_path(start_tile, end_tile, map, heuristic):
    open = [start_tile]
    came_from = {}
    g_scores = {}
    f_scores = {}

    g_scores[start_tile] = 0
    f_scores[start_tile] = heuristic(start_tile, end_tile)

    while len(open) > 0:
        current_tile = open.pop(0)

        if current_tile == end_tile:
            return reconstruct_path(start_tile, end_tile, came_from)

        for neighbour_tile in get_neighbour_tiles(current_tile):
            if neighbour_tile in map.corrupted_tiles or is_tile_outside_map(neighbour_tile, map):
                continue

            tentative_g = g_scores[current_tile] + 1

            if neighbour_tile not in g_scores or tentative_g <= g_scores[neighbour_tile]:
                if neighbour_tile in open:
                    open.remove(neighbour_tile)

                came_from[neighbour_tile] = current_tile
                g_scores[neighbour_tile] = tentative_g
                f_scores[neighbour_tile] = tentative_g + heuristic(neighbour_tile, end_tile)

                bisect.insort(open, neighbour_tile, key=functools.cmp_to_key(lambda tile_a, tile_b: compare_tiles(tile_a, tile_b, f_scores)))

    return None

def reconstruct_path(start_tile, end_tile, came_from):
    path = [end_tile]

    while path[-1] != start_tile:
        path.append(came_from[path[-1]])

    return path[::-1]

def is_tile_on_map(tile, map):
    return 0 <= tile[0] < map.size and 0 <= tile[1] < map.size

def is_tile_outside_map(tile, map):
    return not is_tile_on_map(tile, map)

def compare_tiles(tile_a, tile_b, f_scores):
    if f_scores[tile_a] == f_scores[tile_b]:
        return 0
    
    if f_scores[tile_a] > f_scores[tile_b]:
        return 1
    
    return -1

def manhattan_distance_heuristic(start_tile, end_tile):
    return abs(start_tile[0] - end_tile[0]) + abs(start_tile[1] - end_tile[1])

def parse_bytes(raw_data):
    return [(int(x_coord), int(y_coord)) for x_coord, y_coord in [line.split(',') for line in raw_data.splitlines()]]

if __name__ == '__main__':
    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(18).inputfile)))