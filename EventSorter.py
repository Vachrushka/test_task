import argparse
import os
import sys
from pathlib import Path
from JsonReader import JsonReader


def get_full_path(file_path):
    if file_path is None:
        return None
    return Path(os.path.abspath(file_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Event sorting and grouping program')

    subparsers = parser.add_subparsers(dest="command")
    parser.add_argument('-i', '--input', type=str, help='Input file (json format), default: input.json')
    parser.add_argument('-o', '--output', type=str, help='Output file (json format), default: output.json')

    args = parser.parse_args()

    if args.command == "help":
        parser.print_help()
        exit(1)
    else:
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)
        default_input_path = Path(script_directory + "/data/input.json")  # значения по умолчанию
        default_output_path = Path(script_directory + "/data/output.json")

        input_file = get_full_path(args.input)
        output_file = get_full_path(args.output)
        #input_file = Path("/data/input.json")
        if output_file is None:  # подготовка выходного файла
            output_file = default_output_path

        if input_file is None and not default_input_path.exists():   # проверка наличия входных файлов
            print('Argument "--input" not passed and default file "/data/input.json" does not exist')
            exit(1)
        elif input_file is None:
            input_file = default_input_path
        elif not input_file.exists():
            print('File "{0}" does not exist'.format(input_file))
            exit(1)

        reader = JsonReader(input_file, output_file)
        reader.load_json_data()
        #reader.list_events.print_events_info()
        #reader.list_events.delete_type_other()
        #reader.list_events.close_data_sort()

        reader.group_by_time_events()
        reader.write_groups_data()

        #reader.write_json_data()  # сериализация листа событий
