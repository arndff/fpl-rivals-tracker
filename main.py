from ManipulateData import ManipulateData

import sys

"""
* Project's title: FPL Rivals Tracker
* Author: @Georgi Arnaudov <jrarnaudov@gmail.com>
* Date created: 26/01/2019
"""


def execute():
    file_path = "data/{}".format(sys.argv[1])
    try:
        mdp = ManipulateData(file_path)
    except FileNotFoundError as e:
        print(e)
        return

    mdp.print_table()

    user_input = input("\nStats menu is about to get loaded. Do you want to proceed? [Y/n] ")

    if user_input == "Y" or user_input == "y":
        mdp.print_stats()
    else:
        print("Abort.")


def main():
    if len(sys.argv) != 2:
        print("File path argument is missing.\n")

    execute()


if __name__ == "__main__":
    main()
