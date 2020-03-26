import sys

from analyzers.transfersanalyzer.TransfersAnalyzerOneManager import TransfersAnalyzerOneManager
from analyzers.transfersanalyzer.TransfersAnalyzerManyManagers import TransfersAnalyzerManyManagers

from fileutils.fileutils import validate_input, select_option_from_menu
from read_input import read_input

"""
* Author: @Georgi Arnaudov 
* Twitter: @FPL_arndff
"""


def validate_args():
    if len(sys.argv) > 2:
        print("You must provide zero or one argument.")
        sys.exit(1)


def init_transfers_analyzer_one_manager():
    team_id = read_input("Enter team ID: ")
    print()

    return TransfersAnalyzerOneManager(team_id)


def init_transfers_analyzer_many_managers():
    league_name = input("Enter league name: ")
    league_id = read_input("Enter league ID: ")
    managers_count = read_input("Managers count to be analyzed: ")
    print()

    return TransfersAnalyzerManyManagers(ids_file="",
                                         league_name=league_name,
                                         league_id=league_id,
                                         managers_count=managers_count)


def execute():
    validate_args()
    transfers_analyzer = None

    if len(sys.argv) == 2:
        if not validate_input(sys.argv[1]):
            sys.exit(1)

        transfers_analyzer = TransfersAnalyzerManyManagers(sys.argv[1])
    else:
        options = ["1. Analyze transfers of one manager",
                   "2. Analyze transfers of many managers from a league"]
        while True:
            exception_msg = "\n[!] Please enter an integer: 1 or 2."
            option = select_option_from_menu(options, exception_msg)

            if option == -1:
                continue

            if option == 1:
                transfers_analyzer = init_transfers_analyzer_one_manager()
                break
            elif option == 2:
                transfers_analyzer = init_transfers_analyzer_many_managers()
                break
            else:
                print("\n[!] Invalid option. Try again!")

    transfers_analyzer.print_table()
    transfers_analyzer.save_output_to_file()


def main():
    execute()

if __name__ == "__main__":
    main()
