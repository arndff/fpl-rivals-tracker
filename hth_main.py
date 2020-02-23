import sys

from analyzers.HthAnalyzer import HthAnalyzer
from fileutils.FileUtils import FileUtils

from read_input import read_input

"""
* Author: @Georgi Arnaudov 
* Twitter: @FPL_arndff
* Date created: 04/02/2019
"""


def validate_args():
    if len(sys.argv) > 2:
        print("The script must be called with 0 or 1 argument.")
        sys.exit(1)


def execute():
    validate_args()

    team_id = read_input("Enter team ID: ")

    if len(sys.argv) == 1:
        hth_analyzer = HthAnalyzer(team_id)
    else:
        if not FileUtils.validate_input(sys.argv[1]):
            sys.exit(1)

        hth_analyzer = HthAnalyzer(team_id, False, sys.argv[1])

    hth_analyzer.print_all_matchups()
    hth_analyzer.save_output_to_file()


def main():
    execute()


if __name__ == "__main__":
    main()
