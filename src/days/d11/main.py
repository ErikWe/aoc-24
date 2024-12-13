def solve(raw_data):
    stones = parse_stones(raw_data)
    
    stones_count_cache = {}

    stone_count_25_blinks = blink_n_times_stones_count(stones, 25, stones_count_cache)
    stone_count_75_blinks = blink_n_times_stones_count(stones, 75, stones_count_cache)

    return stone_count_25_blinks, stone_count_75_blinks

def blink_n_times_stones_count(stones, n, stones_count_cache):
    if n == 0:
        return len(stones)
    
    return sum([blink_n_times_stones_count_single_stone(stone, n, stones_count_cache) for stone in stones])

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

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(11).inputfile)))