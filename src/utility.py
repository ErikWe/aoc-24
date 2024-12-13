import argparse
import functools

def count_items_with_filter(list, filter):
    return functools.reduce(lambda sum, value: sum + (1 if filter(value) else 0), list, 0)

def try_parse_int(source):
    if source.isdigit() is False:
        return False, None

    try:
        return True, int(source)
    except ValueError:
        return False, None

def parse_args_day(day):
    parser = argparse.ArgumentParser(description=f'Advent of Code 2024 - Day {day:02d}')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

def read_data(inputfile):
    return open(inputfile, 'r', encoding='utf-8-sig').read()

def print_results(results):
    print(f'{results[0]} | {results[1]}')