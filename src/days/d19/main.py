def solve(raw_data):
    available_towels, towel_patterns = parse_towels(raw_data)

    pattern_solutions_counts = [count_pattern_solutions(towel_pattern, available_towels, {}) for towel_pattern in towel_patterns]

    possible_patterns_count = sum([1 if pattern_solutions_count > 0 else 0 for pattern_solutions_count in pattern_solutions_counts])

    return possible_patterns_count, sum(pattern_solutions_counts)

def count_pattern_solutions(towel_pattern, available_towels, pattern_solutions_counts_by_pattern):
    if towel_pattern == '':
        return 1
    
    if towel_pattern in pattern_solutions_counts_by_pattern:
        return pattern_solutions_counts_by_pattern[towel_pattern]
    
    pattern_solutions_counts_by_pattern[towel_pattern] = sum([count_pattern_solutions(towel_pattern[len(towel):], available_towels, pattern_solutions_counts_by_pattern) for towel in available_towels if towel_pattern.startswith(towel)])

    return pattern_solutions_counts_by_pattern[towel_pattern]

def parse_towels(raw_data):
    available_towels = raw_data.splitlines()[0].split(', ')

    towel_patterns = raw_data.splitlines()[2:]

    return available_towels, towel_patterns

if __name__ == '__main__':
    import sys
    
    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(19).inputfile)))