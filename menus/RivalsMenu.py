from menus.Menu import Menu


class RivalsMenu:
    def __init__(self, data, curr_event):
        self.__data = data
        self.__curr_event = curr_event

    """
    # This method prints a menu and returns a tuple which contains:
    # user choice and a string associated with it
    """
    @staticmethod
    def menu():
        option = -1
        result = (-1, "")

        while option != 1 and option != 2:
            options = ["\n* How do you want to sort the sample by:",
                       "1) Total points",
                       "2) Gameweek points"]
            exception_msg = "\n[!] Please enter an *integer*: either 1 or 2."

            option = Menu.menu(options, exception_msg)

            if option == -1:
                continue
            if option == 1:
                result = (1, "overall_rank")
            elif option == 2:
                result = (2, "gw_points")
            else:
                print("\n[!] Invalid option. Try again!")

        return result

    def stats_menu(self):
        while True:
            options = ["\n* Please choose an option from 1 to 8:",
                       "1) Most captained players",
                       "2) Most vice-captained players",
                       "3) Chips usage during the whole season",
                       "4) Chips usage during GW{}".format(self.__curr_event),
                       "5) Count of managers made at least one transfer",
                       "6) Count of managers took at least one hit",
                       "7) Richest manager(s)",
                       "8) Poorest manager(s)",
                       "9) Exit"]
            exception_msg = "\n[!] Please enter an integer from 1 to 8."

            option = Menu.menu(options, exception_msg)

            if option == -1:
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
                self.__team_value(max)
            elif option == 8:
                self.__team_value(min)
            elif option == 9:
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
            print("No manager has used any chip in GW{}".format(self.__curr_event))
        else:
            self.print_chips(active_chips)

    def __count_managers_who_made_a_transfer(self):
        result = len(list(filter(lambda x: x.gw_transfers > 0, self.__data)))

        if result == 1:
            print("1 manager")
        else:
            print("{} managers".format(result))

    def __count_managers_who_took_a_hit(self):
        result = len(list(filter(lambda x: x.gw_hits > 0, self.__data)))
        print("{} managers".format(result))

    def __team_value(self, f):
        team_values = list(map(lambda x: x.team_value + x.money_itb, self.__data))
        max_value = f(team_values)

        richest_managers = list(filter(lambda x: x.team_value + x.money_itb == max_value, self.__data))
        richest_managers_names = (list(map(lambda x: x.manager_name, richest_managers)))

        result = ', '.join(richest_managers_names)
        print("{} ({}M)".format(result, format(max_value, '.1f')))
