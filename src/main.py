import argparse
import importlib
import sys

sys.path.append("../..")

from utility import print_results, read_data

def parse_args():
    parser = argparse.ArgumentParser(description=f'Advent of Code 2024')
    parser.add_argument('day', type=int, help='The day to solve')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    raw_data = read_data(args.inputfile)

    day_module = importlib.import_module(f'days.d{args.day:02d}.main')

    print_results(day_module.solve(raw_data))