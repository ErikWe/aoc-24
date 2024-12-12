def solve(raw_data):
    text_rows = raw_data.split('\n')

    print(f'{count_spellings(text_rows, count_xmas_at)} | {count_spellings(text_rows, count_x_mas_at)}')

def count_spellings(text_rows, strategy):
    return sum([count_spellings_in_row(y_coord, text_rows, strategy) for y_coord in range(len(text_rows))])

def count_spellings_in_row(y_coord, text_rows, strategy):
    return sum([strategy(x_coord, y_coord, text_rows) for x_coord in range(len(text_rows[y_coord]))])

def count_xmas_at(x_coord, y_coord, text_rows):
    count = 0
    
    for x_delta in [-1, 0, 1]:
        for y_delta in [-1, 0, 1]:
            x_coords = [x_coord + x_delta * delta_idx for delta_idx in range(4)]
            y_coords = [y_coord + y_delta * delta_idx for delta_idx in range(4)]

            if does_sequence_spell_xmas(x_coords, y_coords, text_rows):
                count += 1
    
    return count

def count_x_mas_at(x_coord, y_coord, text_rows):
    return 1 if is_x_mas_at(x_coord, y_coord, text_rows) else 0

def is_x_mas_at(x_coord, y_coord, text_rows):
    return is_x_mas_rightslash_at(x_coord, y_coord, text_rows) and is_x_mas_leftslash_at(x_coord, y_coord, text_rows)

def is_x_mas_rightslash_at(x_coord, y_coord, text_rows):
    x_coords = [x_coord - 1, x_coord, x_coord + 1]
    y_coords = [y_coord + 1, y_coord, y_coord - 1]

    return does_sequence_spell_mas_either_direction(x_coords, y_coords, text_rows)

def is_x_mas_leftslash_at(x_coord, y_coord, text_rows):
    x_coords = [x_coord - 1, x_coord, x_coord + 1]
    y_coords = [y_coord - 1, y_coord, y_coord + 1]

    return does_sequence_spell_mas_either_direction(x_coords, y_coords, text_rows)

def does_sequence_spell_xmas(x_coords, y_coords, text_rows):
    return does_sequence_spell(x_coords, y_coords, text_rows, 'XMAS')

def does_sequence_spell_mas_either_direction(x_coords, y_coords, text_rows):
    return does_sequence_spell(x_coords, y_coords, text_rows, 'MAS') or does_sequence_spell(x_coords, y_coords, text_rows, 'SAM')

def does_sequence_spell(x_coords, y_coords, source_text_rows, target_text):
    if len(x_coords) != len(target_text) or len(y_coords) != len(target_text):
        return False

    return all([0 <= y_coord < len(source_text_rows) and 0 <= x_coords < len(source_text_rows[y_coord]) and source_text_rows[y_coord][x_coords] == target for x_coords, y_coord, target in zip(x_coords, y_coords, target_text)])

if __name__ == '__main__':
    import sys

    sys.path.append(f'{__file__}/../../..')

    from utility import parse_args_day, read_data

    args = parse_args_day(4)

    raw_data = read_data(args.inputfile)

    solve(raw_data)