from Menu import Menu


class FileManager:

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
                FileManager.generate_file_with_ids()
            elif option == 2:
                FileManager.modify_an_existing_file()
            else:
                print("\n[!] Invalid option. Try again!")

    @staticmethod
    def files_helper(msg, mode):
        file_name = input(msg)
        path = "data/{}.txt".format(file_name)
        out = open(path, mode)

        count = int(input("Enter how many IDs do you want to add: "))

        while count > 0:
            next_id = input("Enter next ID: ")
            out.write("{}\n".format(next_id))
            count -= 1

        out.close()

        if mode == "w":
            print("You've successfully generated a file with rivals IDs.")
            print("Its name is: {}".format(file_name))
        elif mode == "a":
            print("You've successfully modified your file.")
            print("Its name is: {}".format(file_name))

    @staticmethod
    def generate_file_with_ids():
        msg = "Enter file name: "
        FileManager.files_helper(msg, "w")

    @staticmethod
    def modify_an_existing_file():
        msg = "Enter file name of an existing file with IDs: "
        FileManager.files_helper(msg, "a")
