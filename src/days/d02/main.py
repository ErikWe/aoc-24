import enum

class Level_Change_Direction(enum.Enum):
    INCREASE = 1
    DECREASE = 2

def solve(raw_data):
    reports = extract_reports(raw_data)

    level_differences = extract_level_differences_from_reports(reports)

    undampened_safe_report_count = count_safe_level_differences(level_differences, 0)
    dampened_safe_report_count = count_safe_level_differences(level_differences, 1)
    
    return undampened_safe_report_count, dampened_safe_report_count

def count_safe_level_differences(level_differences, dampener_count):
    return sum([determine_level_differences_safety(level_difference, dampener_count) for level_difference in level_differences])

def determine_level_differences_safety(level_differences, dampener_count):
    change_directions = [Level_Change_Direction.INCREASE, Level_Change_Direction.DECREASE]

    return any([determine_level_differences_safety_with_direction(level_differences, change_direction, dampener_count) for change_direction in change_directions])

def determine_level_differences_safety_with_direction(level_differences, change_direction, dampener_limit):
    if dampener_limit > 0 and determine_level_differences_safety_with_direction(level_differences[1:], change_direction, dampener_limit - 1):
        return True
    
    for i, level_difference in enumerate(level_differences):

        if are_level_differences_safe(level_difference, change_direction):
            continue

        if dampener_limit == 0:
            return False

        if i != 0 and determine_level_differences_safety_with_direction(dampen_level(i - 1, level_differences)[i - 1:], change_direction, dampener_limit - 1):
            return True

        if i == len(level_differences) - 1 or determine_level_differences_safety_with_direction(dampen_level(i, level_differences)[i:], change_direction, dampener_limit - 1):
            return True

        return False
        
    return True

def dampen_level(i_level, level_differences):
    level_differences = level_differences.copy()

    level_differences[i_level + 1] += level_differences[i_level]

    del level_differences[i_level]

    return level_differences

def are_level_differences_safe(level_difference, change_direction):
    if change_direction == Level_Change_Direction.DECREASE:
        return are_level_differences_safe(level_difference * -1, Level_Change_Direction.INCREASE)

    return level_difference > 0 and level_difference <= 3

def extract_level_differences_from_reports(reports):
    return [extract_level_differences_from_report(report) for report in reports]

def extract_level_differences_from_report(report):
    return [report[i] - report[i - 1] for i in range(1, len(report))]

def extract_reports(raw_data):
    return [[int(component) for component in raw_row.split()] for raw_row in raw_data.splitlines()]

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, print_results, read_data

    print_results(solve(read_data(parse_args_day(2).inputfile)))