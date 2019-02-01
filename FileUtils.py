from Menu import Menu

import re
import sys


class FileUtils:
    @staticmethod
    def menu():
        option = 0

        while option != 1 and option != 2:
            options = ["> What do you want to do:",
                       "1) Generate a new file with rivals IDs",
                       "2) Add more IDs to an existing file"]
            exception_msg = "\n[!] Please enter an *integer*: either 1 or 2."

            option = Menu.menu(options, exception_msg)

            if option == -1:
                continue
            if option == 1:
                FileUtils.generate_file_with_ids()
            elif option == 2:
                FileUtils.modify_an_existing_file()
            else:
                print("\n[!] Invalid option. Try again!")

    @staticmethod
    def files_helper(msg, mode):
        file_name = input(msg)
        path = "data/{}.txt".format(file_name)

        with open(path, mode) as out:
            count = int(input("Enter how many IDs do you want to add: "))
            print()

            while count > 0:
                next_id = input("Enter next ID: ")
                out.write("{}\n".format(next_id))
                count -= 1

            print()

            if mode == "w":
                print("You've successfully generated a file with rivals IDs.")
            elif mode == "a":
                print("You've successfully modified your file.")

            print("Relative path to your file is: data/{}.txt".format(file_name))

    @staticmethod
    def generate_file_with_ids():
        msg = "Enter file name: "
        FileUtils.files_helper(msg, "w")

    @staticmethod
    def modify_an_existing_file():
        msg = "Enter file name of an existing file with IDs: "
        FileUtils.files_helper(msg, "a")

    """
    This method is used to check whether the given file is structured correctly
    It returns the length of wrong_lines list:
    - if the result is 0 -> the file is ok
    """
    @staticmethod
    def validate_input(path, wrong_lines):
        try:
            with open(path, "r") as in_:
                pattern = r"^[1-9][0-9]*$"
                lines = in_.readlines()

                line_number = 1

                for line in lines:
                    if not re.match(pattern, line):
                        wrong_lines.append(line_number)

                    line_number += 1

                return len(wrong_lines)

        except FileNotFoundError:
            print("A problem occurs while opening your file...")
            print("Please check whether file path is correct and try to run main.py again.")
            sys.exit(1)
