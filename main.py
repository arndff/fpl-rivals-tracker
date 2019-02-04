import sys

from fileutils.FileUtils import FileUtils
from analyzers.ClassicAnalyzer import ClassicAnalyzer


"""
* Project's title: FPL Rivals Tracker
* Author: @Georgi Arnaudov <jrarnaudov@gmail.com>
* Date created: 26/01/2019
"""


def execute():
    if not FileUtils.validate_input(sys.argv[1]):
        return

    analyzer = ClassicAnalyzer(sys.argv[1])
    analyzer.print_table()

    user_input = input("\nStats menu is about to get loaded. Do you want to proceed? [Y/n] ")

    if user_input == "Y" or user_input == "y":
        analyzer.print_stats()
    else:
        print("Abort.")


def main():
    if len(sys.argv) != 2:
        print("File path argument is missing.")
        sys.exit(1)

    execute()


if __name__ == "__main__":
    main()
