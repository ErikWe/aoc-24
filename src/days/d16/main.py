import bisect
import functools
import math
import sys

sys.path.append(f'{__file__}/../../..')

from utility import Direction_2d, get_next_tile, turn_clockwise, turn_counter_clockwise

class Map:
    def __init__(self, start_tile, end_tile, wall_tiles):
        self.start_tile = start_tile
        self.end_tile = end_tile
        self.wall_tiles = wall_tiles

def solve(raw_data):
    map = parse_map(raw_data)

    shortest_path_score, came_from, f_scores = find_shortest_paths(map, heuristic)
    tiles_on_shortest_paths_count = count_tiles_on_shortest_paths(map.end_tile, came_from, f_scores)

    return shortest_path_score, tiles_on_shortest_paths_count

def count_tiles_on_shortest_paths(end_tile, came_from, f_scores):
    minimum_f_score = min([f_score for state, f_score in f_scores.items() if state[0] == end_tile])

    states = set()

    for direction in [Direction_2d.EAST, Direction_2d.SOUTH, Direction_2d.WEST, Direction_2d.NORTH]:
        if (end_tile, direction) in f_scores and f_scores[(end_tile, direction)] == minimum_f_score:
            states.update(get_states_on_shortest_paths_to_state((end_tile, direction), came_from))

    return len(set([state[0] for state in states]))

def get_states_on_shortest_paths_to_state(end_state, came_from):
    states = set([end_state])

    if end_state not in came_from:
        return states

    for state in came_from[end_state]:
        if state not in states:
            states.update(get_states_on_shortest_paths_to_state(state, came_from))

    return states

def find_shortest_paths(map, heuristic):
    minimum_f_score = math.inf

    open = [(map.start_tile, Direction_2d.EAST)]
    came_from = {}
    g_scores = {}
    f_scores = {}

    g_scores[(map.start_tile, Direction_2d.EAST)] = 0
    f_scores[(map.start_tile, Direction_2d.EAST)] = heuristic(map.start_tile, Direction_2d.EAST, map.end_tile)

    while len(open) > 0:
        current_state = open.pop(0)

        if f_scores[current_state] > minimum_f_score:
            break

        if current_state[0] == map.end_tile:
            minimum_f_score = f_scores[current_state]
            continue
        
        move_forward_neighbour = ((get_next_tile(current_state[0], current_state[1]), current_state[1]), 1)
        turn_clockwise_neighbour = ((current_state[0], turn_clockwise(current_state[1])), 1000)
        turn_counter_clockwise_neighbour = ((current_state[0], turn_counter_clockwise(current_state[1])), 1000)

        for neighbour_state, d in [move_forward_neighbour, turn_clockwise_neighbour, turn_counter_clockwise_neighbour]:
            if neighbour_state[0] in map.wall_tiles:
                continue

            tentative_g = g_scores[current_state] + d

            if neighbour_state not in g_scores or tentative_g <= g_scores[neighbour_state]:
                if neighbour_state in open:
                    open.remove(neighbour_state)

                if neighbour_state not in g_scores or tentative_g < g_scores[neighbour_state]:
                    came_from[neighbour_state] = []

                came_from[neighbour_state].append(current_state)
                g_scores[neighbour_state] = tentative_g
                f_scores[neighbour_state] = tentative_g + heuristic(neighbour_state[0], neighbour_state[1], map.end_tile)

                bisect.insort(open, neighbour_state, key=functools.cmp_to_key(lambda state_a, state_b: compare_states(state_a, state_b, f_scores)))

    return (minimum_f_score, came_from, f_scores)

def compare_states(state_a, state_b, f_scores):
    if f_scores[state_a] == f_scores[state_b]:
        return 0
    
    if f_scores[state_a] > f_scores[state_b]:
        return 1
    
    return -1

def heuristic(tile, direction, end_tile):
    if tile == end_tile:
        return 0
    
    forward_tile = get_next_tile(tile, direction)

    original_squared_distance = (tile[0] - end_tile[0]) ** 2 + (tile[1] - end_tile[1]) ** 2
    forward_squared_distance = (forward_tile[0] - end_tile[0]) ** 2 + (forward_tile[1] - end_tile[1]) ** 2

    if forward_squared_distance < original_squared_distance:
        return 1 + heuristic(forward_tile, direction, end_tile)
    
    turn_clockwise_tile = get_next_tile(tile, turn_clockwise(direction))
    turn_clockwise_squared_distance = (turn_clockwise_tile[0] - end_tile[0]) ** 2 + (turn_clockwise_tile[1] - end_tile[1]) ** 2

    if turn_clockwise_squared_distance < original_squared_distance:
        return 1000 + heuristic(tile, turn_clockwise(direction), end_tile)
    
    return 1000 + heuristic(tile, turn_counter_clockwise(direction), end_tile)

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

    return Map(start_tile, end_tile, wall_positions)

if __name__ == '__main__':
    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(16).inputfile)))