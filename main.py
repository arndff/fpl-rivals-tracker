import sys

from analyzers.ClassicAnalyzer import ClassicAnalyzer
from fileutils.fileutils import validate_input
from read_input import read_input

"""
* Project's title: FPL Rivals Tracker
* Author: @Georgi Arnaudov
* Twitter: @FPL_arndff
* Date created: 26/01/2019
"""


def validate_args():
    if len(sys.argv) > 2:
        print("You must provide no more than 1 argument.")
        sys.exit(1)


def load_stats_menu(analyzer):
    user_input = input("\nStats menu is about to get loaded. Do you want to proceed? [Y/n] ")

    if user_input == "Y" or user_input == "y":
        analyzer.print_stats()
    else:
        print("Abort.")
        sys.exit(0)


def execute():
    validate_args()

    classic_analyzer = None

    if len(sys.argv) == 1:
        league_name = input("Enter league name: ")
        league_id = read_input("Enter league ID: ")
        managers_count = read_input("Managers count to be analyzed: ")
        print()

        classic_analyzer = ClassicAnalyzer(ids_file="",
                                           league_name=league_name,
                                           league_id=league_id,
                                           managers_count=managers_count)

    if len(sys.argv) == 2:
        if not validate_input(sys.argv[1]):
            sys.exit(1)

        classic_analyzer = ClassicAnalyzer(sys.argv[1])

    classic_analyzer.print_table()
    classic_analyzer.save_output_to_file()

    load_stats_menu(classic_analyzer)


def find_manager_id_by_name():
    validate_args()

    if not validate_input(sys.argv[1]):
        sys.exit(1)

    manager_name = input("Enter manager's name: ")

    classic_analyzer = ClassicAnalyzer(sys.argv[1])
    team_id = classic_analyzer.find_manager_id(manager_name)

    print()

    if team_id != -1:
        print("{}'s ID is: {}".format(manager_name, team_id))
    else:
        print("That manager doesn't exist in your input file with IDs.")


def main():
    execute()
    # find_manager_id_by_name()


if __name__ == "__main__":
    main()
