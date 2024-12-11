import argparse
import math

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

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

def main(raw_data):
    map, antenna_locations_by_frequency = parse_map(raw_data)

    non_harmonic_antinode_locations_by_frequency = compute_antinode_map(map, antenna_locations_by_frequency, non_harmonic_antinode_strategy)
    harmonic_antinode_locations_by_frequency = compute_antinode_map(map, antenna_locations_by_frequency, harmonic_antinode_strategy)

    tiles_with_non_harmonic_antinodes_count = count_tiles_with_antinodes(non_harmonic_antinode_locations_by_frequency)
    tiles_with_harmonic_antinodes_count = count_tiles_with_antinodes(harmonic_antinode_locations_by_frequency)

    report_tiles_with_non_harmonic_antinodes_count(tiles_with_non_harmonic_antinodes_count)
    report_tiles_with_harmonic_antinodes_count(tiles_with_harmonic_antinodes_count)

def report_tiles_with_non_harmonic_antinodes_count(tiles_with_antinodes_count):
    print(f'The number of tiles with antinodes, without considering harmonics, is: {tiles_with_antinodes_count}')

def report_tiles_with_harmonic_antinodes_count(tiles_with_antinodes_count):
    print(f'The number of tiles with antinodes, while considering harmonics, is: {tiles_with_antinodes_count}')

def count_tiles_with_antinodes(antinode_locations_by_frequency):
    tiles_with_antinodes = set()

    for antinode_locations in antinode_locations_by_frequency.values():
        for antinode_location in antinode_locations:
            tiles_with_antinodes.add(antinode_location)

    return len(tiles_with_antinodes)

def non_harmonic_antinode_strategy(antenna_a, antenna_b, map):
    antinode_a = Tile(2 * antenna_a.x_coord - antenna_b.x_coord, 2 * antenna_a.y_coord - antenna_b.y_coord)
    antinode_b = Tile(2 * antenna_b.x_coord - antenna_a.x_coord, 2 * antenna_b.y_coord - antenna_a.y_coord)

    if is_on_map(antinode_a, map):
        yield antinode_a

    if is_on_map(antinode_b, map):
        yield antinode_b

def harmonic_antinode_strategy(antenna_a, antenna_b, map):
    antenna_delta_x = antenna_b.x_coord - antenna_a.x_coord
    antenna_delta_y = antenna_b.y_coord - antenna_a.y_coord

    gcd = math.gcd(antenna_delta_x, antenna_delta_y)

    step_delta_x = antenna_delta_x // gcd
    step_delta_y = antenna_delta_y // gcd

    yield antenna_a

    antinode = Tile(antenna_a.x_coord - step_delta_x, antenna_a.y_coord - step_delta_y)

    while is_on_map(antinode, map):
        yield antinode
        
        antinode = Tile(antinode.x_coord - step_delta_x, antinode.y_coord - step_delta_y)
        
    antinode = Tile(antinode.x_coord + step_delta_x, antinode.y_coord + step_delta_y)

    while is_on_map(antinode, map):
        yield antinode

        antinode = Tile(antinode.x_coord + step_delta_x, antinode.y_coord + step_delta_y)

def compute_antinode_map(map, antenna_locations_by_frequency, antinode_strategy):
    antinode_locations_by_frequency = {}

    for frequency, antenna_locations in antenna_locations_by_frequency.items():
        if len(antenna_locations) < 2:
            continue

        antinodes = []
        
        for i, antenna_a in enumerate(antenna_locations[:-1]):
            for antenna_b in antenna_locations[i + 1:]:
                antinodes.extend(antinode_strategy(antenna_a, antenna_b, map))

        antinode_locations_by_frequency[frequency] = antinodes

    return antinode_locations_by_frequency

def is_on_map(tile, map):
    return map.width > tile.x_coord >= 0 and map.height > tile.y_coord >= 0

def is_outside_map(tile, map):
    return is_on_map(tile, map) is False

def parse_map(raw_data):
    antenna_locations_by_frequency = {}

    text_rows = raw_data.split('\n')

    for y_coord, text_row in enumerate(text_rows):
        for x_coord, tile_character in enumerate(text_row):
            if tile_character == '.':
                continue

            if tile_character not in antenna_locations_by_frequency:
                antenna_locations_by_frequency[tile_character] = []

            antenna_locations_by_frequency[tile_character].append(Tile(x_coord, y_coord))

    return Map(len(text_rows[0]), len(text_rows)), antenna_locations_by_frequency

def parse_args():
    parser = argparse.ArgumentParser(description='Advent of Code 2024 - Day 08')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

args = parse_args()

raw_data = open(args.inputfile, 'r', encoding='utf-8-sig').read()

main(raw_data)