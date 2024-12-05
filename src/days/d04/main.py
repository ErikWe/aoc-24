import argparse

def main(raw_text):
    text_rows = extract_rows_from_text(raw_text)

    xmas_count = count_xmas_in_all_rows(text_rows)
    x_mas_count = count_x_mas_in_all_rows(text_rows)

    report_xmas_count(xmas_count)
    report_x_mas_count(x_mas_count)

def report_xmas_count(xmas_count):
    print(f'XMAS occurrences: {xmas_count}')

def report_x_mas_count(x_mas_count):
    print(f'X-MAS occurrences: {x_mas_count}')

def count_xmas_in_all_rows(text_rows):
    return sum([count_xmas_in_row(y_coord, text_rows) for y_coord in range(len(text_rows))])

def count_x_mas_in_all_rows(text_rows):
    return sum([count_x_mas_in_row(y_coord, text_rows) for y_coord in range(len(text_rows))])

def count_xmas_in_row(y_coord, text_rows):
    return sum([count_xmas_at(x_coord, y_coord, text_rows) for x_coord in range(len(text_rows[y_coord]))])

def count_x_mas_in_row(y_coord, text_rows):
    return sum([spells_x_mas_at(x_coord, y_coord, text_rows) for x_coord in range(len(text_rows[y_coord]))])

def count_xmas_at(x_coord, y_coord, text_rows):
    count = 0
    
    for x_delta in [-1, 0, 1]:
        for y_delta in [-1, 0, 1]:
            x_coords = [x_coord + x_delta * delta_idx for delta_idx in range(4)]
            y_coords = [y_coord + y_delta * delta_idx for delta_idx in range(4)]


            if sequence_spells_xmas(x_coords, y_coords, text_rows):
                count += 1
    
    return count

def spells_x_mas_at(x_coord, y_coord, text_rows):
    return spells_x_mas_slash_at(x_coord, y_coord, text_rows) and spells_x_mas_backslash_at(x_coord, y_coord, text_rows)

def spells_x_mas_slash_at(x_coord, y_coord, text_rows):
    x_coords = [x_coord - 1, x_coord, x_coord + 1]
    y_coords = [y_coord + 1, y_coord, y_coord - 1]

    return sequence_spells_mas_either_direction(x_coords, y_coords, text_rows)

def spells_x_mas_backslash_at(x_coord, y_coord, text_rows):
    x_coords = [x_coord - 1, x_coord, x_coord + 1]
    y_coords = [y_coord - 1, y_coord, y_coord + 1]

    return sequence_spells_mas_either_direction(x_coords, y_coords, text_rows)

def sequence_spells_xmas(x_coords, y_coords, text_rows):
    return sequence_spells(x_coords, y_coords, text_rows, "XMAS")

def sequence_spells_mas_either_direction(x_coords, y_coords, text_rows):
    return sequence_spells_mas(x_coords, y_coords, text_rows) or sequence_spells_mas_backwards(x_coords, y_coords, text_rows)

def sequence_spells_mas(x_coords, y_coords, text_rows):
    return sequence_spells(x_coords, y_coords, text_rows, "MAS")

def sequence_spells_mas_backwards(x_coords, y_coords, text_rows):
    return sequence_spells(x_coords, y_coords, text_rows, "SAM")

def sequence_spells(x_coords, y_coords, source_text_rows, target_text):
    if len(x_coords) != len(target_text) or len(y_coords) != len(target_text):
        return False

    return all([0 <= y_coord < len(source_text_rows) and 0 <= x_coords < len(source_text_rows[y_coord]) and source_text_rows[y_coord][x_coords] == target for x_coords, y_coord, target in zip(x_coords, y_coords, target_text)])

def extract_rows_from_text(raw_text):
    return raw_text.split('\n')

def parse_args():
    parser = argparse.ArgumentParser(description='Advent of Code 2024 - Day 04')
    parser.add_argument('inputfile', help='The file containing the input data')

    return parser.parse_args()

args = parse_args()

raw_text = open(args.inputfile, 'r').read()

main(raw_text)