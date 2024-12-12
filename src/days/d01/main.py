import sys

sys.path.append(f'{__file__}/../../..')

from utility import count_items_with_filter

def solve(raw_data):
    group_a_ids, group_b_ids = extract_ids(raw_data)

    print(f'{compute_summed_difference(group_a_ids, group_b_ids)} | {compute_summed_similarity(group_a_ids, group_b_ids)}')

def compute_summed_similarity(group_a_ids, group_b_ids):
    return sum([id * count_occurrences_of_id(id, group_b_ids) for id in group_a_ids])

def compute_summed_difference(group_a_ids, group_b_ids):
    return sum([abs(a - b) for a, b in zip(sorted(group_a_ids), sorted(group_b_ids))])

def count_occurrences_of_id(target_id, ids):
    return count_items_with_filter(ids, lambda actual_id: actual_id == target_id)

def extract_ids(raw_data):
    ids = [[int(component) for component in raw_row.split()] for raw_row in raw_data.split('\n')]

    return [id[0] for id in ids], [id[1] for id in ids]

if __name__ == '__main__':
    from utility import parse_args_day, read_data

    args = parse_args_day(1)

    raw_data = read_data(args.inputfile)

    solve(raw_data)