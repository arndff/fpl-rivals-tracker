from analyzers.AutosubsAnalyzer import AutosubsAnalyzer

from read_input import read_input

"""
* Author: @Georgi Arnaudov 
* Twitter: @FPL_arndff
"""


def execute():
    team_id = read_input("Enter team ID: ")
    print()

    autosubs_analyzer = AutosubsAnalyzer(team_id)
    autosubs_analyzer.print_table()
    autosubs_analyzer.save_output_to_file()


def main():
    execute()


if __name__ == "__main__":
    main()
