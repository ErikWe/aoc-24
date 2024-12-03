import argparse
import sys

sys.path.append("../..")

from utility import count_items_with_filter

def main(raw_data):
    group_a, group_b = extract_ids(raw_data)

    summed_difference = compute_summed_difference(group_a, group_b)
    summed_similarity = compute_summed_similarity(group_a, group_b)

    report_summed_difference(summed_difference)
    report_summed_similarity(summed_similarity)

def report_summed_similarity(similarity):
    print(f'The summed similarity between the two groups is: {similarity}')

def report_summed_difference(difference):
    print(f'The summed difference between the two groups is: {difference}')

def compute_summed_similarity(group_a, group_b):
    similarity = [id * count_occurrences_of_id(id, group_b) for id in group_a]

    return sum(similarity)

def compute_summed_difference(group_a, group_b):
    group_a_sorted = sort_ids(group_a)
    group_b_sorted = sort_ids(group_b)

    differences = [abs(a - b) for a, b in zip(group_a_sorted, group_b_sorted)]

    return sum(differences)

def sort_ids(ids):
    return sorted(ids)

def count_occurrences_of_id(target_id, ids):
    return count_items_with_filter(ids, lambda actual_id: actual_id == target_id)

def extract_ids(raw_data):
    ids = [extract_ids_from_row(raw_row) for raw_row in raw_data.split('\n')]

    return [id[0] for id in ids], [id[1] for id in ids]

def extract_ids_from_row(raw_row):
    components = raw_row.split()

    return [int(components[0]), int(components[1])]

def parse_args():
    parser = argparse.ArgumentParser(description='Advent of Code 2024 - Day 01')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

args = parse_args()

raw_data = open(args.inputfile, 'r').read()

main(raw_data)