import json
import sys

from analyzers.MiniLeagueAnalyzer import MiniLeagueAnalyzer

"""
* Author: @Georgi Arnaudov 
* Twitter: @FPL_arndff
"""


def read_league_id():
    league_id = -1

    while league_id == -1:
        try:
            league_id = int(input("Enter league's ID: "))
        except ValueError:
            print("Please enter a valid integer! Try again.\n")

    return league_id


def read_file_name():
    file_name = input("Enter file's name: ")
    print()

    return file_name


def read_data():
    league_id = read_league_id()
    file_name = read_file_name()
    result = (league_id, file_name)

    return result


def config(person):
    with open("config/mini_league_analyzer_config.json", "r") as read_file:
        data = json.load(read_file)

    main_dir = data["main_dir"]
    save_path = "{}/{}"

    person_data = data[person]
    result = (person_data["file_name"], person_data["league_id"],
              save_path.format(main_dir, person), person_data["ids_file"])

    return result


def execute():
    if len(sys.argv) == 1:
        (league_id, file_name) = read_data()
        mini_league_analyzer = MiniLeagueAnalyzer(file_name, league_id)
        mini_league_analyzer.write_data_to_csv()
    else:
        try:
            (file_name, league_id, save_path, ids_file) = config(sys.argv[1].lower())

            if ids_file != "":
                mini_league_analyzer = MiniLeagueAnalyzer(file_name, league_id, save_path, ids_file)
                mini_league_analyzer.write_data_to_csv()
                print()

            if league_id != -1:
                mini_league_analyzer = MiniLeagueAnalyzer(file_name, league_id, save_path)
                mini_league_analyzer.write_data_to_csv()

        except KeyError:
            print("That key hasn't been found in the config file.")
            print("Please enter your data manually.\n")

            (league_id, file_name) = read_data()
            mini_league_analyzer = MiniLeagueAnalyzer(file_name, league_id)
            mini_league_analyzer.write_data_to_csv()


def main():
    execute()


if __name__ == "__main__":
    main()
