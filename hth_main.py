import sys

from analyzers.HthAnalyzer import HthAnalyzer

"""
* Author: @Georgi Arnaudov <jrarnaudov@gmail.com>
* Date created: 04/02/2019
"""


def execute():
    while True:
        try:
            team_id = int(input("Enter your team ID: "))
        except ValueError:
            print("Please enter a valid integer! Try again.\n")
            continue

        print("You're going to see your different players in each H2H match this GW. It'll take a few seconds...\n")

        if len(sys.argv) == 1:
            hth_analyzer = HthAnalyzer(team_id)
        else:
            hth_analyzer = HthAnalyzer(team_id, False, sys.argv[1])

        hth_analyzer.print_all_matchups()

        print("Good luck, {}! :)".format(hth_analyzer.manager_name))
        break


def main():
    if len(sys.argv) > 2:
        print("The script must be called with 0 or 1 argument.")
        sys.exit(1)

    execute()


if __name__ == "__main__":
    main()
