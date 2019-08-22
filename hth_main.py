import sys

from analyzers.HthAnalyzer import HthAnalyzer
from fileutils.FileUtils import FileUtils

"""
* Author: @Georgi Arnaudov <jrarnaudov@gmail.com>
* Date created: 04/02/2019
"""


def execute():
    if len(sys.argv) > 2:
        print("The script must be called with 0 or 1 argument.")
        sys.exit(1)

    team_id = -1

    while team_id == -1:
        try:
            team_id = int(input("Enter your team ID: "))
            print()
        except ValueError:
            print("Please enter a valid integer! Try again.\n")

    if len(sys.argv) == 1:
        hth_analyzer = HthAnalyzer(team_id)
    else:
        if not FileUtils.validate_input(sys.argv[1]):
            sys.exit(1)

        hth_analyzer = HthAnalyzer(team_id, False, sys.argv[1])

    hth_analyzer.print_all_matchups()
    print("Good luck, {}! :)".format(hth_analyzer.manager_name))


def main():
    execute()


if __name__ == "__main__":
    main()
