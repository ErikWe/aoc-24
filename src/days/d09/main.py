def solve(raw_data):
    storage_blocks = parse_storage(raw_data)

    fragmented_checksum = compute_checksum(optimize_storage_with_fragmentation(storage_blocks.copy()))
    non_fragmented_checksum = compute_checksum(optimize_storage_without_fragmentation(storage_blocks.copy()))

    print(f'{fragmented_checksum} | {non_fragmented_checksum}')

def compute_checksum(storage_blocks):
    return sum([i * storage_block for i, storage_block in enumerate(storage_blocks) if storage_block != -1])

def optimize_storage_with_fragmentation(storage_blocks):
    i_empty_slot = -1
    i_data_slot = len(storage_blocks)

    while True:
        i_empty_slot = find_next_slot(i_empty_slot, storage_blocks, storage_slot_is_empty)
        i_data_slot = find_previous_slot(i_data_slot, storage_blocks, storage_slot_is_not_empty)

        if i_empty_slot < 0 or i_data_slot < 0 or i_empty_slot >= i_data_slot:
            break

        storage_blocks[i_empty_slot] = storage_blocks[i_data_slot]
        storage_blocks[i_data_slot] = -1

    return storage_blocks

def optimize_storage_without_fragmentation(storage_blocks):
    excluded_count_by_empty_length = []

    file_id = storage_blocks[find_previous_slot(len(storage_blocks), storage_blocks, storage_slot_is_not_empty)]
    i_file_end = len(storage_blocks)
    file_length = -1

    while True:
        if file_id < 0:
            break

        i_file_end = find_previous_slot(i_file_end, storage_blocks, storage_slot_is_not_empty)

        file_length = find_file_length_from_end(i_file_end, storage_blocks)

        if storage_blocks[i_file_end] == file_id:
            file_id -= 1
                    
            excluded_count = get_excluded_count_for_empty_length(file_length, excluded_count_by_empty_length)

            while True:
                excluded_count = find_next_slot(excluded_count - 1, storage_blocks, storage_slot_is_empty)

                empty_length = find_empty_storage_length_from_start(excluded_count, storage_blocks)

                if excluded_count >= i_file_end - file_length:
                    break

                if empty_length >= file_length:
                    move_file(i_file_end, file_length, excluded_count, storage_blocks)
                    force_update_excluded_count(empty_length, excluded_count + file_length, excluded_count_by_empty_length)
                    break

                excluded_count += empty_length

        i_file_end -= file_length - 1

    return storage_blocks

def move_file(i_file_end, file_length, i_empty_start, storage_blocks):
    for i in range(file_length):
        storage_blocks[i_empty_start + i] = storage_blocks[i_file_end - i]
        storage_blocks[i_file_end - i] = -1

def get_excluded_count_for_empty_length(empty_length, excluded_count_by_empty_length):
    if len(excluded_count_by_empty_length) > empty_length:
        return excluded_count_by_empty_length[empty_length]

    if len(excluded_count_by_empty_length) == 0:
        return 0

    return excluded_count_by_empty_length[-1]

def force_update_excluded_count(empty_length, excluded_count, excluded_count_by_empty_length):
    extend_excluded_count_by_empty_length(empty_length, excluded_count_by_empty_length)

    for hypothetical_empty_length in range(empty_length, len(excluded_count_by_empty_length)):
        if excluded_count_by_empty_length[hypothetical_empty_length] > excluded_count:
            break

        excluded_count_by_empty_length[hypothetical_empty_length] = excluded_count

def extend_excluded_count_by_empty_length(empty_length, excluded_count_by_empty_length):
    if len(excluded_count_by_empty_length) > empty_length:
        return
    
    if len(excluded_count_by_empty_length) == 0:
        excluded_count_by_empty_length.extend([0] * (empty_length + 1))
        return
    
    excluded_count_by_empty_length.extend([excluded_count_by_empty_length[-1]] * (empty_length - len(excluded_count_by_empty_length) + 1))

def find_file_length_from_end(i_file_end, storage_blocks):
    i_empty_end = find_previous_slot(i_file_end, storage_blocks, get_end_of_file_condition(storage_blocks[i_file_end]))

    if i_empty_end < 0:
        return i_file_end + 1
    
    return i_file_end - i_empty_end

def find_empty_storage_length_from_start(i_empty_start, storage_blocks):
    i_file_start = find_next_slot(i_empty_start, storage_blocks, storage_slot_is_not_empty)

    if i_file_start < 0:
        return len(storage_blocks) - i_empty_start
    
    return i_file_start - i_empty_start

def find_next_slot(i, storage_blocks, condition):
    while i < len(storage_blocks) - 1:
        if condition(storage_blocks[i + 1]):
            return i + 1
        
        i += 1

    return -1

def find_previous_slot(i, storage_blocks, condition):
    while i > 0:
        if condition(storage_blocks[i - 1]):
            return i - 1
        
        i -= 1

    return -1

def storage_slot_is_empty(storage_slot):
    return storage_slot == -1

def storage_slot_is_not_empty(storage_slot):
    return storage_slot != -1

def get_end_of_file_condition(file_id):
    return lambda storage_slot: storage_slot_is_empty(storage_slot) or storage_slot != file_id

def parse_storage(raw_data):
    storage_blocks = []

    for i, formatted in enumerate(raw_data):
        data_length = int(formatted)

        if i % 2 == 1:
            storage_blocks.extend([-1 for _ in range(data_length)])

        if i % 2 == 0:
            storage_blocks.extend([i // 2 for _ in range(data_length)])

    return storage_blocks

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, read_data

    args = parse_args_day(9)

    raw_data = read_data(args.inputfile)

    solve(raw_data)