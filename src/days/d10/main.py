import argparse

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

def main(raw_data):
    heights = parse_map(raw_data)

    all_trailhead_endings = resolve_trailhead_endings(get_all_trailhead_endings(heights))

    total_trailhead_score = score_all_trailheads(all_trailhead_endings, score_trailhead_strategy)
    total_trailhead_rating = score_all_trailheads(all_trailhead_endings, rate_trailhead_strategy)

    report_total_trailhead_score(total_trailhead_score)
    report_total_trailhead_rating(total_trailhead_rating)

def report_total_trailhead_score(total_trailhead_score):
    print(f'The total trailhead score is: {total_trailhead_score}')

def report_total_trailhead_rating(total_trailhead_rating):
    print(f'The total trailhead rating is: {total_trailhead_rating}')

def score_all_trailheads(all_trailhead_endings, strategy):
    total_score = 0

    for trailhead_endings in all_trailhead_endings:
        total_score += strategy(trailhead_endings)

    return total_score

def resolve_trailhead_endings(trailhead_endings_generator):
    return [[trailhead_ending for trailhead_ending in trailhead_endings] for trailhead_endings in trailhead_endings_generator]

def get_all_trailhead_endings(heights):
    for y_coord, row_heights in enumerate(heights):
        for x_coord, height in enumerate(row_heights):
            if height == 0:
                yield get_trailends(Tile(x_coord, y_coord), heights)

def score_trailhead_strategy(trailhead_endings):
    return len(set(trailhead_endings))

def rate_trailhead_strategy(trailhead_endings):
    return len(trailhead_endings)

def get_trailends(source_tile, heights):
    source_height = heights[source_tile.y_coord][source_tile.x_coord]

    if source_height == 9:
        yield source_tile
        return

    target_tiles = [get_tile_north(source_tile), get_tile_south(source_tile), get_tile_west(source_tile), get_tile_east(source_tile)]

    for target_tile in target_tiles:
        if is_on_map(target_tile, heights) and heights[target_tile.y_coord][target_tile.x_coord] == source_height + 1:
            yield from get_trailends(target_tile, heights)

def is_on_map(tile, heights):
    return 0 <= tile.y_coord < len(heights) and 0 <= tile.x_coord < len(heights[tile.y_coord])

def get_tile_north(tile):
    return Tile(tile.x_coord, tile.y_coord - 1)

def get_tile_south(tile):
    return Tile(tile.x_coord, tile.y_coord + 1)

def get_tile_west(tile):
    return Tile(tile.x_coord - 1, tile.y_coord)

def get_tile_east(tile):
    return Tile(tile.x_coord + 1, tile.y_coord)

def parse_map(raw_data):
    heights = []

    for line in raw_data.split('\n'):
        row_heights = []

        for height in line:
            row_heights.append(int(height))

        heights.append(row_heights)

    return heights

def parse_args():
    parser = argparse.ArgumentParser(description='Advent of Code 2024 - Day 10')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

args = parse_args()

raw_data = open(args.inputfile, 'r', encoding='utf-8-sig').read()

main(raw_data)