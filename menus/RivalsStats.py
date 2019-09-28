from fileutils.FileUtils import FileUtils
from menus.Menu import Menu


class RivalsStats:
    def __init__(self, data, curr_event, output_file_name):
        self.__data = data
        self.__current_event = curr_event
        self.__output_file_name = output_file_name

        self.__output = []

        self.__options = self.__init_options()
        self.__append_options_to_output()

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

    def save_stats_output_to_file(self):
        FileUtils.save_classic_output_to_file(self.__output_file_name, "a+", self.__output)

    def stats_menu(self):
        while True:
            exception_msg = "\n[!] Please enter an integer from 1 to 10."

            option = Menu.menu(self.__options, exception_msg)
            self.__output.append("Selected option: {}".format(option))

            if option == -1:
                continue

            if option == 1:
                self.__calculate_average_points()
            elif option == 2:
                self.__print_captains((list(map(lambda x: x.captain_name, self.__data))))
            elif option == 3:
                self.__print_captains((list(map(lambda x: x.vice_captain_name, self.__data))))
            elif option == 4:
                self.__print_chip_usage_whole_season()
            elif option == 5:
                self.__print_chip_usage_current_event()
            elif option == 6:
                self.__count_managers_made_transfer()
            elif option == 7:
                self.__count_managers_took_hit()
            elif option == 8:
                self.__print_team_value(max)
            elif option == 9:
                self.__print_team_value(min)
            elif option == 10:
                self.__output.append("")
                break

            else:
                print("\n[!] Invalid option. Try again!")

    @staticmethod
    def init_a_dict(key, dictionary):
        if key not in dictionary:
            dictionary[key] = 1
        else:
            dictionary[key] += 1

    def print_chips(self, chips):
        for chip in chips:
            string = "{}({})".format(chip, chips[chip])
            print(string, end=" ")
            self.__output.append(string)

        print()
        self.__output.append("")

    def __init_options(self):
        options = ["\n* Please choose an option from 1 to 10:",
                   "1) Sample's average score",
                   "2) Most captained players",
                   "3) Most vice-captained players",
                   "4) Chips usage during the whole season",
                   "5) Chips usage during GW{}".format(self.__current_event),
                   "6) Count of managers made at least one transfer",
                   "7) Count of managers took at least one hit",
                   "8) Richest manager(s)",
                   "9) Poorest manager(s)",
                   "10) Exit"]

        return options

    def __calculate_average_points(self):
        managers_count = len(self.__data)
        total_points = 0

        for manager in self.__data:
            total_points += manager.gw_points()
            total_points -= manager.gw_hits

        average_points = total_points / managers_count
        result = "{:.2f} points".format(average_points)

        print(result)
        self.__output.append(result)
        self.__output.append("")

    def __print_captains(self, list_of_captains):
        captains = {}

        for captain in list_of_captains:
            self.init_a_dict(captain, captains)

        captains_sorted = [(captain, captains[captain]) for captain in sorted(captains, key=captains.get, reverse=True)]

        for key, value in captains_sorted:
            captain = "{}({})".format(key, value)
            print(captain, end=" ")
            self.__output.append(captain)

        print()
        self.__output.append("")

    # TO-DO: Test
    def __print_chip_usage_whole_season(self):
        chips = {}

        for manager in self.__data:
            for chip in manager.used_chips_by_gw:
                self.init_a_dict(chip, chips)

        self.print_chips(chips)

    def __print_chip_usage_current_event(self):
        active_chips = {}

        for manager in self.__data:
            active_chip = manager.active_chip

            if active_chip != "None":
                self.init_a_dict(active_chip, active_chips)

        if len(active_chips) < 1:
            result = "No manager has used any chip in GW{}".format(self.__current_event)
            self.__log_string(result)
        else:
            self.print_chips(active_chips)

    def __count_managers_made_transfer(self):
        result = len(list(filter(lambda x: x.gw_transfers > 0, self.__data)))

        if result == 1:
            managers_count = "1 manager"
        else:
            managers_count = "{} managers".format(result)

        self.__log_string(managers_count)

    def __count_managers_took_hit(self):
        result = len(list(filter(lambda x: x.gw_hits > 0, self.__data)))
        managers_count = "{} managers".format(result)
        self.__log_string(managers_count)

    def __print_team_value(self, f):
        team_values = list(map(lambda x: x.team_value, self.__data))
        max_value = f(team_values)

        richest_managers = list(filter(lambda x: x.team_value == max_value, self.__data))
        richest_managers_names = (list(map(lambda x: x.manager_name, richest_managers)))

        result = ', '.join(richest_managers_names)

        result_string = "{} ({}M)".format(result, format(max_value, '.1f'))
        self.__log_string(result_string)

    def __append_options_to_output(self):
        self.__output.append("")
        [self.__output.append(option) for option in self.__options]
        self.__output.append("")

    def __log_string(self, string):
        print(string)
        self.__output.append(string)
        self.__output.append("")
