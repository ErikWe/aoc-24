import sys

sys.path.append(f'{__file__}/../../..')

from utility import Direction_2d, get_next_tile

class Map:
    def __init__(self, robot_position, box_positions, wall_positions):
        self.robot_position = robot_position
        self.box_positions = box_positions
        self.wall_positions = wall_positions

def solve(raw_data):
    narrow_map = parse_map(raw_data.split('\n\n')[0], 1)
    wide_map = parse_map(raw_data.split('\n\n')[0], 2)

    moves = parse_moves(raw_data.split('\n\n')[1])

    make_moves(moves, narrow_map, 1)
    make_moves(moves, wide_map, 2)

    narrow_total_gps_coordinates = compute_total_gps_coordinates(narrow_map)
    wide_total_gps_coordinates = compute_total_gps_coordinates(wide_map)

    return narrow_total_gps_coordinates, wide_total_gps_coordinates

def compute_total_gps_coordinates(map):
    return sum([box_position[0] + 100 * box_position[1] for box_position in map.box_positions])

def make_moves(moves, map, width_scale):
    for move in moves:
        try_make_move(map.robot_position, move, map, width_scale)

def try_make_move(tile, move, map, width_scale):
    next_tile = get_next_tile(tile, move)

    if next_tile in map.wall_positions:
        return False
    
    box_on_tile = get_box_on_tile(next_tile, map, width_scale)
    
    if box_on_tile != None:
        new_map = Map(map.robot_position, map.box_positions.copy(), map.wall_positions)

        if move == Direction_2d.NORTH or move == Direction_2d.SOUTH:
            for offset in range(width_scale - 1, -1, -1):
                if try_make_move((box_on_tile[0] + offset, box_on_tile[1]), move, new_map, width_scale) is False:
                    return False
            
        if move == Direction_2d.WEST:
            if try_make_move((next_tile[0] - width_scale + 1, next_tile[1]), move, new_map, width_scale) is False:
                return False
            
        if move == Direction_2d.EAST:
            if try_make_move((next_tile[0] + width_scale - 1, next_tile[1]), move, new_map, width_scale) is False:
                return False

        map.box_positions = new_map.box_positions
        map.box_positions.remove(box_on_tile)
        map.box_positions.add(get_next_tile(box_on_tile, move))

    if tile == map.robot_position:
        map.robot_position = next_tile

    return True
        
def get_box_on_tile(tile, map, width_scale):
    for offset in range(width_scale):
        if (tile[0] - offset, tile[1]) in map.box_positions:
            return (tile[0] - offset, tile[1])

def parse_map(raw_data, width_scale):
    robot_position = None
    box_positions = set()
    wall_positions = set()

    for y_coord, line in enumerate(raw_data.splitlines()):
        for unscaled_x_coord, content in enumerate(line):
            scaled_x_coord = unscaled_x_coord * width_scale

            if content == '@':
                robot_position = (scaled_x_coord, y_coord)
            
            if content == '#':
                for offset in range(width_scale):
                    wall_positions.add((scaled_x_coord + offset, y_coord))
            
            if content == 'O':
                box_positions.add((scaled_x_coord, y_coord))

    return Map(robot_position, box_positions, wall_positions)

def parse_moves(raw_data):
    moves = []
    
    for move in raw_data:
        if move == '<':
            moves.append(Direction_2d.WEST)
        if move == '>':
            moves.append(Direction_2d.EAST)
        if move == '^':
            moves.append(Direction_2d.NORTH)
        if move == 'v':
            moves.append(Direction_2d.SOUTH)

    return moves

if __name__ == '__main__':
    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(15).inputfile)))