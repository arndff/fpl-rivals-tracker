from analyzers.CaptainPicksAnalyzer import CaptainPickAnalyzer
from read_input import read_input

"""
* Author: @Georgi Arnaudov 
* Twitter: @FPL_arndff
"""


def execute():
    team_id = read_input("Enter team ID: ")
    print()

    captain_picks_analyzer = CaptainPickAnalyzer(team_id)
    captain_picks_analyzer.print_table()
    # captain_picks_analyzer.save_output_to_file()


def main():
    execute()


if __name__ == "__main__":
    main()
