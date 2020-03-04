import json
import sys

from analyzers.MiniLeagueAnalyzer import MiniLeagueAnalyzer
from read_input import read_input

"""
* Author: @Georgi Arnaudov 
* Twitter: @FPL_arndff
"""


def read_league_data():
    league_name = input("Enter league name: ")
    league_id = read_input("Enter league id: ")

    result = (league_name, league_id)
    return result


def load_config(key):
    person = key.split("-")[1]

    with open("config/mini_league_analyzer_config.json", "r") as read_file:
        all_data = json.load(read_file)

    main_dir = all_data.get("main_dir", "")
    save_dir = "{}/{}".format(main_dir, person)

    data = all_data.get(person, "")
    ids_file = data.get("ids_file", "")
    league_name = data.get("league_name", "")
    league_id = data.get("league_id", -1)

    result = (ids_file, save_dir, league_name, league_id)
    return result


def create_analyzer_objects(key):
    (ids_file, save_dir, league_name, league_id) = load_config(key)
    print(ids_file, save_dir, league_name, league_id)
    analyzers = []

    if ids_file != "":
        analyzers.append(MiniLeagueAnalyzer(ids_file=ids_file, save_dir=save_dir))
    if league_id != -1:
        analyzers.append(MiniLeagueAnalyzer(ids_file="",
                                            save_dir=save_dir,
                                            league_name=league_name,
                                            league_id=league_id))

    return analyzers


def execute():
    if len(sys.argv) == 2 and sys.argv[1].startswith("config-"):
        analyzers = create_analyzer_objects(sys.argv[1])
        [mini_league_analyzer.write_data_to_csv() for mini_league_analyzer in analyzers]
    else:
        if len(sys.argv) == 2:
            mini_league_analyzer = MiniLeagueAnalyzer(ids_file=sys.argv[1])
        elif len(sys.argv) == 3:
            mini_league_analyzer = MiniLeagueAnalyzer(ids_file=sys.argv[1], save_dir=sys.argv[2])
        else:
            (league_id, league_name) = read_league_data()
            mini_league_analyzer = MiniLeagueAnalyzer(ids_file="",
                                                      save_dir="",
                                                      league_name=league_name,
                                                      league_id=league_id)

        mini_league_analyzer.write_data_to_csv()


def main():
    execute()


if __name__ == "__main__":
    main()
