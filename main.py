import sys

from analyzers.ClassicAnalyzer import ClassicAnalyzer
from fileutils.FileUtils import FileUtils


"""
* Project's title: FPL Rivals Tracker
* Author: @Georgi Arnaudov
* Twitter: @FPL_arndff
* Date created: 26/01/2019
"""


def validate_args():
    if len(sys.argv) == 1:
        print("File path argument is missing.")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("You must provide exactly one argument.")
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

    if not FileUtils.validate_input(sys.argv[1]):
        sys.exit(1)

    analyzer = ClassicAnalyzer(sys.argv[1])
    analyzer.print_table()
    analyzer.save_output_to_file()

    load_stats_menu(analyzer)


def find_manager_id_by_name():
    manager_name = input("Enter manager's name: ")

    validate_args()

    if not FileUtils.validate_input(sys.argv[1]):
        sys.exit(1)

    analyzer = ClassicAnalyzer(sys.argv[1])
    manager_id = analyzer.find_manager_id(manager_name)

    if manager_id != -1:
        print("{}'s ID is: {}".format(manager_name, manager_id))
    else:
        print("That manager doesn't exist in your input file.")


def main():
    execute()
    # find_manager_id_by_name()


if __name__ == "__main__":
    main()
