import functools

def solve(raw_data):
    rules_text, updates_text = raw_data.split("\n\n")

    rules = read_all_rules(rules_text)
    allowed_upcoming_pages_per_page = get_allowed_upcoming_pages_per_page(rules)

    updates = read_all_updates(updates_text)
    update_validities = get_update_validities(updates, allowed_upcoming_pages_per_page)

    valid_updates_middle_page_sum = sum_middle_pages_of_updates(get_valid_updates(updates, update_validities))
    fixed_invalid_updates_middle_page_sum = sum_middle_pages_of_updates(sort_updates(get_invalid_updates(updates, update_validities), allowed_upcoming_pages_per_page))

    print(f'{valid_updates_middle_page_sum} | {fixed_invalid_updates_middle_page_sum}')

def sort_updates(updates, allowed_upcoming_pages_per_page):
    return [sort_update(update, allowed_upcoming_pages_per_page) for update in updates]

def sort_update(update, allowed_upcoming_pages_per_page):
    return sorted(update, key=functools.cmp_to_key(lambda page_a, page_b: compare_pages(page_a, page_b, allowed_upcoming_pages_per_page)))

def compare_pages(page_a, page_b, allowed_upcoming_pages_per_page):
    return 1 if page_a in allowed_upcoming_pages_per_page and page_b in allowed_upcoming_pages_per_page[page_a] else -1

def sum_middle_pages_of_updates(updates):
    return sum(get_middle_pages_of_updates(updates))

def get_middle_pages_of_updates(updates):
    return [get_middle_page_of_update(update) for update in updates]

def get_valid_updates(updates, update_validities):
    return get_updates_with_validity(updates, update_validities, True)

def get_invalid_updates(updates, update_validities):
    return get_updates_with_validity(updates, update_validities, False)

def get_updates_with_validity(updates, update_validities, validity):
    return [update for update, update_validity in zip(updates, update_validities) if update_validity == validity]

def get_update_validities(updates, allowed_upcoming_pages_per_page):
    return [is_update_valid(update, allowed_upcoming_pages_per_page) for update in updates]

def is_update_valid(update, allowed_upcoming_pages_per_page):
    for i in range(len(update) - 1):
        for j in range(i + 1, len(update)):
            if update[i] not in allowed_upcoming_pages_per_page or update[j] not in allowed_upcoming_pages_per_page[update[i]]:
                return False
            
    return True

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

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, read_data

    args = parse_args_day(5)

    raw_data = read_data(args.inputfile)

    solve(raw_data)