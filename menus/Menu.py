class Menu:

    @staticmethod
    def main_menu():
        pass

    @staticmethod
    def menu(options, exception_message):
        [print(op, sep='\n') for op in options]
        option = -1

        try:
            option = int(input("\n> Enter the desired option's number: "))
        except ValueError:
            print(exception_message)

        return option
