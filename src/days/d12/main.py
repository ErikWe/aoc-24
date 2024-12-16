import sys

sys.path.append(f'{__file__}/../../..')

from utility import get_neighbour_tiles, get_neighbour_tiles_with_direction, get_next_tile, turn_clockwise, turn_counter_clockwise

def solve(raw_data):
    map = parse_map(raw_data)

    plots = extract_all_plots(map)

    undiscounted_total_price = compute_total_price(plots, compute_undiscounted_plot_price)
    discounted_total_price = compute_total_price(plots, compute_discounted_plot_price)

    return undiscounted_total_price, discounted_total_price

def extract_all_plots(unfenced_tiles):
    plots = []

    while len(unfenced_tiles) > 0:
        plots.append(extract_plot(list(unfenced_tiles.keys())[0], unfenced_tiles))

    return plots

def extract_plot(tile, unfenced_tiles):
    tiles = set([tile])

    plant_type = unfenced_tiles[tile]

    del unfenced_tiles[tile]

    for neighbour in get_neighbour_tiles(tile):
        if neighbour in unfenced_tiles and unfenced_tiles[neighbour] == plant_type:
            tiles.update(extract_plot(neighbour, unfenced_tiles))

    return tiles

def compute_total_price(plots, price_strategy):
    return sum([price_strategy(plot) for plot in plots])

def compute_undiscounted_plot_price(plot):
    perimeter = 0

    for tile in plot:
        for neighbour in get_neighbour_tiles(tile):
            if neighbour not in plot:
                perimeter += 1

    return perimeter * len(plot)

def compute_discounted_plot_price(plot):
    perimeter = set()

    for tile in plot:
        for neighbour_with_direction in get_neighbour_tiles_with_direction(tile):
            if neighbour_with_direction[0] not in plot:
                perimeter.add((tile, neighbour_with_direction[1]))

    edge_turns = 0

    for tile, direction in perimeter:
        right_tile = get_next_tile(tile, turn_clockwise(direction))
        left_tile = get_next_tile(tile, turn_counter_clockwise(direction))

        if (right_tile, direction) not in perimeter:
            edge_turns += 1

        if (left_tile, direction) not in perimeter:
            edge_turns += 1

    return edge_turns // 2 * len(plot)

def parse_map(raw_data):
    map = {}

    for y_coord, line in enumerate(raw_data.splitlines()):
        for x_coord, plant_type in enumerate(line):
            map[(x_coord, y_coord)] = plant_type

    return map

if __name__ == '__main__':
    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(12).inputfile)))