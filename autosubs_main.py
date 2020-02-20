from analyzers.AutosubsAnalyzer import AutosubsAnalyzer

"""
* Author: @Georgi Arnaudov 
* Twitter: @FPL_arndff
"""


def read_input():
    team_id = -1

    while team_id == -1:
        try:
            team_id = int(input("Enter team ID: "))
            print()
        except ValueError:
            print("Please enter a valid integer! Try again.\n")

    return team_id


def execute():
    team_id = read_input()

    autosubs_analyzer = AutosubsAnalyzer(team_id)
    autosubs_analyzer.print_table()
    autosubs_analyzer.save_output_to_file()


def main():
    execute()


if __name__ == "__main__":
    main()
