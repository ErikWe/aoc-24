def solve(raw_data):
    heights = parse_map(raw_data)

    all_trailhead_endings = resolve_trailhead_endings(get_all_trailhead_endings(heights))

    trailhead_score = score_all_trailheads(all_trailhead_endings, score_trailhead_strategy)
    trailhead_rate = score_all_trailheads(all_trailhead_endings, rate_trailhead_strategy)

    return trailhead_score, trailhead_rate

def score_all_trailheads(all_trailhead_endings, strategy):
    return sum([strategy(trailhead_endings) for trailhead_endings in all_trailhead_endings])

def resolve_trailhead_endings(trailhead_endings_generator):
    return [[trailhead_ending for trailhead_ending in trailhead_endings] for trailhead_endings in trailhead_endings_generator]

def get_all_trailhead_endings(heights):
    for y_coord, row_heights in enumerate(heights):
        for x_coord, height in enumerate(row_heights):
            if height == 0:
                yield get_trailends((x_coord, y_coord), heights)

def score_trailhead_strategy(trailhead_endings):
    return len(set(trailhead_endings))

def rate_trailhead_strategy(trailhead_endings):
    return len(trailhead_endings)

def get_trailends(source_tile, heights):
    source_height = heights[source_tile[1]][source_tile[0]]

    if source_height == 9:
        yield source_tile
        return

    target_tiles = [get_tile_north(source_tile), get_tile_south(source_tile), get_tile_west(source_tile), get_tile_east(source_tile)]

    for target_tile in target_tiles:
        if is_on_map(target_tile, heights) and heights[target_tile[1]][target_tile[0]] == source_height + 1:
            yield from get_trailends(target_tile, heights)

def is_on_map(tile, heights):
    return 0 <= tile[1] < len(heights) and 0 <= tile[0] < len(heights[tile[1]])

def get_tile_north(tile):
    return (tile[0], tile[1] - 1)

def get_tile_south(tile):
    return (tile[0], tile[1] + 1)

def get_tile_west(tile):
    return (tile[0] - 1, tile[1])

def get_tile_east(tile):
    return (tile[0] + 1, tile[1])

def parse_map(raw_data):
    heights = []

    for line in raw_data.splitlines():
        row_heights = []

        for height in line:
            row_heights.append(int(height))

        heights.append(row_heights)

    return heights

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(10).inputfile)))