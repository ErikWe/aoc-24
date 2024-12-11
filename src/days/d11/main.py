import argparse

def main(raw_data):
    stones = parse_stones(raw_data)

    stones_count_cache = {}

    stones_after_25_blinks_count = blink_n_times_stones_count(stones, 25, stones_count_cache)
    stones_after_75_blinks_count = blink_n_times_stones_count(stones, 75, stones_count_cache)

    report_stones_after_n_blinks_count(stones_after_25_blinks_count, 25)
    report_stones_after_n_blinks_count(stones_after_75_blinks_count, 75)

def report_stones_after_n_blinks_count(stones_count, n):
    print(f'After {n} blinks, there are {stones_count} stones')

def blink_n_times_stones_count(stones, n, stones_count_cache):
    if n == 0:
        return len(stones)
    
    sum = 0

    for stone in stones:
        sum += blink_n_times_stones_count_single_stone(stone, n, stones_count_cache)

    return sum

def blink_n_times_stones_count_single_stone(stone, n, stones_count_cache):
    if (stone, n) in stones_count_cache:
        return stones_count_cache[(stone, n)]
    
    stones = blick_once_single_stone(stone)

    count = blink_n_times_stones_count(stones, n - 1, stones_count_cache)

    stones_count_cache[(stone, n)] = count

    return count

def blick_once_single_stone(stone):
    if stone == 0:
        return [1]
    
    stone_text = str(stone)

    if len(stone_text) % 2 == 0:
        return [int(stone_text[:len(stone_text) // 2]), int(stone_text[len(stone_text) // 2:])]
    
    return [stone * 2024]

def parse_stones(raw_data):
    return [int(x) for x in raw_data.split()]

def parse_args():
    parser = argparse.ArgumentParser(description='Advent of Code 2024 - Day 11')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

args = parse_args()

raw_data = open(args.inputfile, 'r', encoding='utf-8-sig').read()

main(raw_data)