import argparse
import enum
import functools

class Update_Validity(enum.Enum):
    VALID = 1
    INVALID = 2

def main(raw_data):
    rules_text, updates_text = raw_data.split("\n\n")

    rules = read_all_rules(rules_text)
    allowed_upcoming_pages_per_page = get_allowed_upcoming_pages_per_page(rules)

    updates = read_all_updates(updates_text)
    update_validities = get_update_validities(updates, allowed_upcoming_pages_per_page)

    valid_updates_middle_page_sum = sum_middle_pages_of_updates(get_valid_updates(updates, update_validities))
    fixed_invalid_updates_middle_page_sum = sum_middle_pages_of_updates(sort_updates(get_invalid_updates(updates, update_validities), allowed_upcoming_pages_per_page))

    report_valid_updates_middle_page_sum(valid_updates_middle_page_sum)
    report_fixed_invalid_updates_middle_page_sum(fixed_invalid_updates_middle_page_sum)

def report_valid_updates_middle_page_sum(valid_updates_middle_page_sum):
    print(f'The sum of the middle pages of valid updates is: {valid_updates_middle_page_sum}')

def report_fixed_invalid_updates_middle_page_sum(fixed_invalid_updates_middle_page_sum):
    print(f'The sum of the middle pages of fixed invalid updates is: {fixed_invalid_updates_middle_page_sum}')

def sort_updates(updates, allowed_upcoming_pages_per_page):
    return [sort_update(update, allowed_upcoming_pages_per_page) for update in updates]

def sort_update(update, allowed_upcoming_pages_per_page):
    return sorted(update, key=functools.cmp_to_key(lambda page_a, page_b: is_page_a_before_page_b(page_a, page_b, allowed_upcoming_pages_per_page)))

def is_page_a_before_page_b(page_a, page_b, allowed_upcoming_pages_per_page):
    if page_a in allowed_upcoming_pages_per_page and page_b in allowed_upcoming_pages_per_page[page_a]:
        return 1
    
    return -1

def sum_middle_pages_of_updates(updates):
    return sum(get_middle_pages_of_updates(updates))

def get_middle_pages_of_updates(updates):
    return [get_middle_page_of_update(update) for update in updates]

def get_valid_updates(updates, update_validities):
    return get_updates_with_validity(updates, update_validities, Update_Validity.VALID)

def get_invalid_updates(updates, update_validities):
    return get_updates_with_validity(updates, update_validities, Update_Validity.INVALID)

def get_updates_with_validity(updates, update_validities, validity):
    return [update for update, update_validity in zip(updates, update_validities) if update_validity == validity]

def get_update_validities(updates, allowed_upcoming_pages_per_page):
    return [get_update_validity(update, allowed_upcoming_pages_per_page) for update in updates]

def get_update_validity(update, allowed_upcoming_pages_per_page):
    for i in range(len(update) - 1):
        for j in range(i + 1, len(update)):
            if update[i] not in allowed_upcoming_pages_per_page or update[j] not in allowed_upcoming_pages_per_page[update[i]]:
                return Update_Validity.INVALID
            
    return Update_Validity.VALID

def get_allowed_upcoming_pages_per_page(rules):
    allowed_upcoming_pages_per_page = {}

    for first_page, last_page in rules:
        if first_page not in allowed_upcoming_pages_per_page:
            allowed_upcoming_pages_per_page[first_page] = set()

        allowed_upcoming_pages_per_page[first_page].add(last_page)

    return allowed_upcoming_pages_per_page

def get_middle_page_of_update(update):
    return update[len(update) // 2]

def read_all_updates(updates_text):
    return read_rows(updates_text, read_update)

def read_update(update_text):
    return [int(page) for page in update_text.split(',')]

def read_all_rules(rules_text):
    return read_rows(rules_text, read_rule)

def read_rule(rule_text):
    return [int(page) for page in rule_text.split('|')]

def read_rows(text, func):
    return [func(row) for row in text.split("\n")]

def parse_args():
    parser = argparse.ArgumentParser(description='Advent of Code 2024 - Day 05')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

args = parse_args()

raw_data = open(args.inputfile, 'r', encoding='utf-8-sig').read()

main(raw_data)