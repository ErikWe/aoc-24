import argparse
import enum
import sys

sys.path.append("../..")

from utility import count_items_with_filter

class Level_change_direction(enum.Enum):
    INCREASE = 1
    DECREASE = 2

def main(raw_data):
    reports = extract_reports(raw_data)

    level_differences_all_reports = [extract_level_differences_from_report(report) for report in reports]

    undampened_safe_reports_count = count_safe_reports(level_differences_all_reports, 0)
    dampened_safe_reports_count = count_safe_reports(level_differences_all_reports, 1)

    report_undampened_safe_reports_count(undampened_safe_reports_count)
    report_dampened_safe_reports_count(dampened_safe_reports_count)

def report_undampened_safe_reports_count(safe_reports_count):
    print(f'Without a dampener, the number of safe reports is: {safe_reports_count}')

def report_dampened_safe_reports_count(safe_reports_count):
    print(f'With a dampener, the number of safe reports is: {safe_reports_count}')

def count_safe_reports(level_differences_all_reports, dampener_limit):
    return count_items_with_filter(level_differences_all_reports, lambda level_difference: determine_level_differences_safety(level_difference, dampener_limit))

def determine_level_differences_safety(level_differences, dampener_limit):
    change_directions = [Level_change_direction.INCREASE, Level_change_direction.DECREASE]

    for change_direction in change_directions:
        if determine_level_differences_safety_with_direction(level_differences, change_direction, dampener_limit):
            return True
        
        if dampener_limit > 0:
            if determine_level_differences_safety_with_direction(level_differences[1:], change_direction, dampener_limit - 1):
                return True

    return False

def determine_level_differences_safety_with_direction(level_differences, change_direction, dampener_limit):
    def with_previous_dampened(i):
        if i == 0:
            return False
        
        adjusted_differences = level_differences[i:]
        adjusted_differences[0] += level_differences[i - 1]

        return determine_level_differences_safety_with_direction(adjusted_differences, change_direction, dampener_limit - 1)

    def with_current_dampened(i):
        if i == len(level_differences) - 1:
            return True

        adjusted_differences = level_differences[(i + 1):]
        adjusted_differences[0] += level_differences[i]

        return determine_level_differences_safety_with_direction(adjusted_differences, change_direction, dampener_limit - 1)

    for i, level_difference in enumerate(level_differences):

        if determine_level_difference_safety(level_difference, change_direction):
            continue

        if dampener_limit == 0:
            return False

        if with_previous_dampened(i):
            return True

        if with_current_dampened(i):
            return True

        return False
        
    return True

def determine_level_difference_safety(level_difference, change_direction):
    if change_direction == Level_change_direction.DECREASE:
        level_difference *= -1

    return level_difference > 0 and level_difference <= 3

def extract_level_differences_from_report(report):
    return [report[i] - report[i - 1] for i in range(1, len(report))]

def extract_reports(raw_data):
    return [extract_levels_from_row(raw_row) for raw_row in raw_data.split('\n')]

def extract_levels_from_row(raw_row):
    return [int(component) for component in raw_row.split()]

def parse_args():
    parser = argparse.ArgumentParser(description='Advent of Code 2024 - Day 02')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

args = parse_args()

raw_data = open(args.inputfile, 'r').read()

main(raw_data)
