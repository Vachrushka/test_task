import argparse
import os
from pathlib import Path

from DataManager import DataManager


def get_full_path(file_path):
    if file_path is None:
        return None
    return Path(os.path.abspath(file_path))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Event sorting and grouping program')
    parser.add_argument('-i', '--input', type=str, default="data/input.json",
                        help='Input file (json format), default: data/input.json')
    parser.add_argument('-o', '--output', type=str, default="data/output.json",
                        help='Output file (json format), default: data/output.json')
    return parser.parse_args()


def main(input_path, output_path):
    manager = DataManager(input_path, output_path)
    manager.load_json_data()

    manager.group_by_time_events()
    manager.write_groups_data()


if __name__ == "__main__":
    args = parse_arguments()

    input_file = Path(args.input)
    output_file = Path(args.output)

    if not input_file.exists():
        print('File "{0}" does not exist'.format(input_file))
        exit(1)

    main(input_file, output_file)
