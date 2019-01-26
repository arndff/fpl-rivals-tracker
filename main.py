import sys
from ManipulateData import ManipulateData


def execute():
    mdp = ManipulateData(sys.argv[1])
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
