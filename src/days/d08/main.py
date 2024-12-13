import math

def solve(raw_data):
    map_dimensions, antenna_locations_by_frequency = parse_map(raw_data)

    tiles_with_non_harmonic_antinodes_count = count_tiles_with_antinodes(compute_antinode_map(map_dimensions, antenna_locations_by_frequency, non_harmonic_antinode_strategy))
    tiles_with_harmonic_antinodes_count = count_tiles_with_antinodes(compute_antinode_map(map_dimensions, antenna_locations_by_frequency, harmonic_antinode_strategy))

    return tiles_with_non_harmonic_antinodes_count, tiles_with_harmonic_antinodes_count

def count_tiles_with_antinodes(antinode_locations_by_frequency):
    tiles_with_antinodes = set()

    for antinode_locations in antinode_locations_by_frequency.values():
        for antinode_location in antinode_locations:
            tiles_with_antinodes.add(antinode_location)

    return len(tiles_with_antinodes)

def non_harmonic_antinode_strategy(antenna_a, antenna_b, map_dimensions):
    antinode_a = (2 * antenna_a[0] - antenna_b[0], 2 * antenna_a[1] - antenna_b[1])
    antinode_b = (2 * antenna_b[0] - antenna_a[0], 2 * antenna_b[1] - antenna_a[1])

    if is_on_map(antinode_a, map_dimensions):
        yield antinode_a

    if is_on_map(antinode_b, map_dimensions):
        yield antinode_b

def harmonic_antinode_strategy(antenna_a, antenna_b, map_dimensions):
    antenna_delta_x = antenna_b[0] - antenna_a[0]
    antenna_delta_y = antenna_b[1] - antenna_a[1]

    gcd = math.gcd(antenna_delta_x, antenna_delta_y)

    step_delta_x = antenna_delta_x // gcd
    step_delta_y = antenna_delta_y // gcd

    yield antenna_a

    antinode = (antenna_a[0] - step_delta_x, antenna_a[1] - step_delta_y)

    while is_on_map(antinode, map_dimensions):
        yield antinode
        
        antinode = (antinode[0] - step_delta_x, antinode[1] - step_delta_y)
        
    antinode = (antinode[0] + step_delta_x, antinode[1] + step_delta_y)

    while is_on_map(antinode, map_dimensions):
        yield antinode

        antinode = (antinode[0] + step_delta_x, antinode[1] + step_delta_y)

def compute_antinode_map(map_dimensions, antenna_locations_by_frequency, antinode_strategy):
    antinode_locations_by_frequency = {}

    for frequency, antenna_locations in antenna_locations_by_frequency.items():
        if len(antenna_locations) < 2:
            continue

        antinodes = []
        
        for i, antenna_a in enumerate(antenna_locations[:-1]):
            for antenna_b in antenna_locations[i + 1:]:
                antinodes.extend(antinode_strategy(antenna_a, antenna_b, map_dimensions))

        antinode_locations_by_frequency[frequency] = antinodes

    return antinode_locations_by_frequency

def is_on_map(tile, map_dimensions):
    return 0 <= tile[0] < map_dimensions[0] and 0 <= tile[1] < map_dimensions[1]

def is_outside_map(tile, map_dimensions):
    return is_on_map(tile, map_dimensions) is False

def parse_map(raw_data):
    antenna_locations_by_frequency = {}

    text_rows = raw_data.splitlines()

    for y_coord, text_row in enumerate(text_rows):
        for x_coord, tile_character in enumerate(text_row):
            if tile_character == '.':
                continue

            if tile_character not in antenna_locations_by_frequency:
                antenna_locations_by_frequency[tile_character] = []

            antenna_locations_by_frequency[tile_character].append((x_coord, y_coord))

    return (len(text_rows[0]), len(text_rows)), antenna_locations_by_frequency

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(8).inputfile)))