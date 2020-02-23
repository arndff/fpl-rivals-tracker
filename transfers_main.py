import sys

from analyzers.TransfersAnalyzer import TransfersAnalyzer
from fileutils.FileUtils import FileUtils

from read_input import read_input

"""
* Author: @Georgi Arnaudov 
* Twitter: @FPL_arndff
"""


def validate_args():
    if len(sys.argv) > 2:
        print("You must provide zero or one argument.")
        sys.exit(1)


def execute():
    validate_args()

    if len(sys.argv) == 2:
        if not FileUtils.validate_input(sys.argv[1]):
            sys.exit(1)

        transfers_analyzer = TransfersAnalyzer(sys.argv[1])
        transfers_analyzer.print_table()
    else:
        ids_file = ""
        team_id = read_input("Enter team ID: ")

        transfers_analyzer = TransfersAnalyzer(ids_file, team_id)
        transfers_analyzer.print_all_transfers()

    transfers_analyzer.save_output_to_file()


def main():
    execute()


if __name__ == "__main__":
    main()
