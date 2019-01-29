class Menu:

    def __init__(self, data, curr_event):
        self.__data = data
        self.__curr_event = curr_event

    """
    # This method prints a menu and returns a tuple which contains:
    # user choice and a string associated with it
    """
    @staticmethod
    def main_menu():
        option = 0
        result = (0, "")

        while option != 1 and option != 2:
            print("\n* How do you want to sort the sample by:",
                  "1) Total points",
                  "2) Gameweek points",
                  sep='\n')

            try:
                option = int(input("\n> Enter the desired option's number: "))
            except ValueError:
                print("\n[!] Please enter an *integer*: either 1 or 2.")
                continue

            if option == 1:
                result = (1, "overall_rank")
            elif option == 2:
                result = (2, "gw_points")
            else:
                print("\n[!] Invalid option. Try again!")

        print("\n")
        return result

    def stats_menu(self):
        while True:
            print("\n* Please choose an option from 1 to 8:",
                  "1) Most captained players",
                  "2) Most vice-captained players",
                  "3) Chips usage during the whole season",
                  "4) Chips usage during GW{}".format(self.__curr_event),
                  "5) How many managers have already made a transfer?",
                  "6) How many managers have already taken a hit?",
                  "7) What's the value of the richest team(s) in the sample?",
                  "8) Exit",
                  sep='\n')

            try:
                option = int(input("\n> Enter the desired option's number: "))
            except ValueError:
                print("\n[!] Please enter an integer from 1 to 8.")
                continue

            if option == 1:
                self.__print_captains_names_and_count((list(map(lambda x: x.captain_name, self.__data))))

            elif option == 2:
                self.__print_captains_names_and_count((list(map(lambda x: x.vice_captain_name, self.__data))))

            elif option == 3:
                self.__print_each_chip_usage_whole_season()

            elif option == 4:
                self.__print_each_chip_usage_in_curr_event()

            elif option == 5:
                self.__count_managers_who_made_a_transfer()

            elif option == 6:
                self.__count_managers_who_took_a_hit()

            elif option == 7:
                self.__richest_team_value()

            elif option == 8:
                break

            else:
                print("\n[!] Invalid option. Try again!")

    @staticmethod
    def init_a_dict(key, dictionary):
        if key not in dictionary:
            dictionary[key] = 1
        else:
            dictionary[key] += 1

    @staticmethod
    def print_chips(chips):
        [print("{}({})".format(chip, chips[chip]), end=" ") for chip in chips]
        print()

    def __print_captains_names_and_count(self, list_of_captains):
        captains = {}

        for captain in list_of_captains:
            self.init_a_dict(captain, captains)

        captains_sorted = [(captain, captains[captain]) for captain in sorted(captains, key=captains.get, reverse=True)]

        for key, value in captains_sorted:
            print("{}({})".format(key, value), end=" ")

        print()

    def __print_each_chip_usage_whole_season(self):
        chips = {}

        for manager in self.__data:
            for chip in manager.used_chips:
                self.init_a_dict(chip, chips)

        self.print_chips(chips)

    def __print_each_chip_usage_in_curr_event(self):
        active_chips = {}

        for manager in self.__data:
            active_chip = manager.active_chip

            if active_chip != "None":
                self.init_a_dict(active_chip, active_chips)

        if len(active_chips) < 1:
            print("No manager has used any chip in GW{}.".format(self.__curr_event))
        else:
            self.print_chips(active_chips)

    def __count_managers_who_made_a_transfer(self):
        res = len(list(filter(lambda x: x.gw_transfers > 0, self.__data)))

        if res == 1:
            print("Result: 1 manager.")
        else:
            print("Result: {} managers.".format(res))

    def __count_managers_who_took_a_hit(self):
        res = len(list(filter(lambda x: x.gw_hits > 0, self.__data)))
        print("Result: {} managers.".format(res))

    def __richest_team_value(self):
        team_values = list(map(lambda x: x.team_value + x.money_itb, self.__data))
        max_value = max(team_values)

        richest_managers = list(filter(lambda x: x.team_value + x.money_itb == max_value, self.__data))
        richest_managers_names = (list(map(lambda x: x.manager_name, richest_managers)))

        res = ', '.join(richest_managers_names)
        print("Result: {} ({}M).".format(res, max_value))
