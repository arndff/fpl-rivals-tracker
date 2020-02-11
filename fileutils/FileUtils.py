import re
import sys

from menus.Menu import menu


class FileUtils:
    @staticmethod
    def menu():
        option = -1
        exit_option = 4

        while option != exit_option:
            options = ["> What do you want to do:",
                       "1) Generate a new file with rivals IDs",
                       "2) Add more IDs to an existing file",
                       "3) Check whether a text file with IDs is valid",
                       "4) Exit"]
            exception_msg = "\n[!] Please enter an *integer*: either 1 or 2."

            option = menu(options, exception_msg)

            if option == -1:
                continue
            if option == 1:
                FileUtils.generate_file_with_ids()
            elif option == 2:
                FileUtils.modify_existing_file()
            elif option == 3:
                path = input("Please, enter file's path: ")
                print()

                if FileUtils.validate_input(path):
                    print("The file has the correct structure.")

            elif option == 4:
                return
            else:
                print("\n[!] Invalid option. Try again!")

            print()

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

            print("The relative path to your file is: data/{}.txt".format(file_name))

    @staticmethod
    def generate_file_with_ids():
        msg = "Enter file name: "
        FileUtils.files_helper(msg, "w")

    @staticmethod
    def modify_existing_file():
        msg = "Enter file name of an existing file with IDs: "
        FileUtils.files_helper(msg, "a")

    @staticmethod
    def validate_input(path):
        wrong_lines = []
        FileUtils.validate_input_helper(path, wrong_lines)
        success = len(wrong_lines)

        if success > 0:
            print("Your file isn't valid! Please fix line(s) with number: ")
            [print(line, end=' ') for line in wrong_lines]
            print()

            return False

        return True

    """
    This method is used to check whether the given file is structured correctly
    It returns the length of wrong_lines list:
    - if the result is 0 -> the file is ok
    """
    @staticmethod
    def validate_input_helper(path, wrong_lines):
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
            print("A problem occurred while opening your file...")
            print("Please check whether file path is correct and try to run main.py again.")
            sys.exit(1)

    # All methods below take care of saving data to file
    @staticmethod
    def save_output_to_file(path, file_mode, output):
        with open(path, file_mode, encoding="utf-8") as out:
            output_len = len(output)

            for i in range(0, output_len-1):
                out.write(output[i])
                out.write("\n")

            out.write(output[output_len-1])

    @staticmethod
    def extract_file_name_from_path(path):
        last_slash = path.rfind("/")

        if last_slash == -1:
            last_slash = path.rfind("\\")

        path_len = len(path)
        extension_len = 4
        file_name = path[last_slash + 1: path_len - extension_len]

        return file_name
