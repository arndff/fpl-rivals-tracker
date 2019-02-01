from FileUtils import FileUtils
from ManipulateData import ManipulateData

import sys

"""
* Project's title: FPL Rivals Tracker
* Author: @Georgi Arnaudov <jrarnaudov@gmail.com>
* Date created: 26/01/2019
"""


def validate_input(path):
    wrong_lines = []
    FileUtils.validate_input(path, wrong_lines)
    success = len(wrong_lines)

    if success > 0:
        print("Your file has a problem! Please fix line(s) with number: ")
        [print(line, end=' ') for line in wrong_lines]
        print()
        return False

    return True


def execute():
    if not validate_input(sys.argv[1]):
        return

    mdp = ManipulateData(sys.argv[1])
    mdp.print_table()

    user_input = input("\nStats menu is about to get loaded. Do you want to proceed? [Y/n] ")

    if user_input == "Y" or user_input == "y":
        mdp.print_stats()
    else:
        print("Abort.")


def main():
    if len(sys.argv) != 2:
        print("File path argument is missing.")
        sys.exit(1)

    execute()


if __name__ == "__main__":
    main()
