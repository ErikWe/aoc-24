import functools

def count_items_with_filter(list, filter):
    return functools.reduce(lambda sum, value: sum + (1 if filter(value) else 0), list, 0)