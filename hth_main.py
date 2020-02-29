import sys

from analyzers.hthanalyzer.HthAnalyzerFromFile import HthAnalyzerFromFile
from analyzers.hthanalyzer.HthAnalyzerLeagues import HthAnalyzerLeagues
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
        hth_analyzer = HthAnalyzerLeagues(team_id)
    else:
        if not FileUtils.validate_input(sys.argv[1]):
            sys.exit(1)

        hth_analyzer = HthAnalyzerFromFile(team_id=team_id, ids_file=sys.argv[1])

    hth_analyzer.print_all_matchups()
    hth_analyzer.save_output_to_file()


def main():
    execute()


if __name__ == "__main__":
    main()
