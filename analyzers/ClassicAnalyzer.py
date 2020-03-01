from functools import cmp_to_key
from operator import attrgetter

from tabulate import tabulate

from analyzers.utility_functions import get_gw_info, read_ids, set_output_file, performance, start_threads
from fileutils.fileutils import log_string, save_output_to_file, select_option_from_menu
from managers.ClassicManager import ClassicManager
from stats.ClassicAnalyzerStats import ClassicAnalyzerStats
from parsers.LiveDataParser import LiveDataParser


class ClassicAnalyzer:
    __LAST_EVENT = 38

    @performance
    def __init__(self, ids_file, league_name="", league_id=-1, managers_count=-1):
        [self.__current_event, self.__gw_name, self.__is_dgw] = get_gw_info()

        self.__ids = read_ids(ids_file, league_id, managers_count)

        self.__live_data_parser = LiveDataParser(self.__current_event, self.__is_dgw)

        self.__managers = self.__init_managers()
        self.__init_each_manager_players_played()

        self.__output = []  # A list which stores the whole output
        self.__output_file = set_output_file(self.__current_event, "rivals", ids_file, league_name, league_id)

    def print_table(self):
        self.__sort_managers()
        self.__format_managers_properties()

        self.__print_legend()
        self.__print_table_output()

    def print_stats(self):
        stats = ClassicAnalyzerStats(self.__managers, self.__current_event, self.__output_file)
        stats.stats_menu()

        stats.save_stats_output_to_file()

    def save_output_to_file(self):
        save_output_to_file(self.__output_file, "w", self.__output)

    def find_manager_id(self, name):
        for manager in self.__managers:
            if manager.manager_name == name:
                return manager.get_id()

        return -1

    @start_threads
    def __init_managers(self):
        threads = list(map(lambda id_: ClassicManager(id_, self.__current_event, self.__is_dgw), self.__ids))
        return threads

    def __init_each_manager_players_played(self):
        for manager in self.__managers:
            (sgw_players_count, dgw_players_info) = self.__live_data_parser.count_players_played(manager.players_ids)
            manager.format_players_played(sgw_players_count)

            if self.__is_dgw:
                manager.format_dgw_players_played(*dgw_players_info)

    def __sort_managers(self):
        """
                menu returns an integer which indicates how the data is going to be sorted by:
                1: total points
                2: gameweek points
                3: team value
                """
        comparator = self.__menu()

        # sort the data
        if comparator[0] == 1:
            self.__managers.sort(key=attrgetter(comparator[1]), reverse=False)
        elif comparator[0] == 2:
            self.__managers.sort(key=cmp_to_key(ClassicManager.cmp_gw_pts))
        else:
            self.__managers.sort(key=attrgetter(comparator[1]), reverse=True)

    """
    # This method prints a menu and returns a tuple which contains:
    # user choice and a string associated with it
    """
    def __menu(self):
        option = -1
        result = (-1, "")

        options_number = {1, 2, 3}

        while option not in options_number:
            options = ["* How do you want to sort the sample by:",
                       "1) Total points",
                       "2) Gameweek points",
                       "3) Total team value"]
            exception_msg = "\n[!] Please enter an *integer*: either 1, 2 or 3."

            option = select_option_from_menu(options, exception_msg)

            if option == -1:
                continue

            if option == 1:
                result = (1, "overall_rank")
            elif option == 2:
                result = (2, "gw_points")
            elif option == 3:
                result = (3, "team_value")

            else:
                print("\n[!] Invalid option. Try again!")

        return result

    def __format_managers_properties(self):
        row_num = 1

        # format some of its columns
        for manager in self.__managers:
            manager.format_total_points_and_overall_rank()
            manager.format_gw_points()

            manager.row_num = row_num
            row_num += 1

    def __init_headers(self):
        headers = ["No", "Manager", "OR", "OP", "Used Chips",
                   "{} P".format(self.__gw_name),
                   "C".format(self.__gw_name),
                   "VC".format(self.__current_event),
                   "Chip".format(self.__current_event),
                   "PP",
                   "{} TM".format(self.__gw_name),
                   "{} H".format(self.__gw_name),
                   "TV", "Bank", "Tot"]

        if self.__is_dgw:
            index = 10
            headers.insert(index, "PP II")

        return headers

    def __print_legend(self):
        print()
        legend = ["> Legend: ",
                  "OR = Overall Rank, OP = Overall Points,\n"
                  "C = Captain, VC = Vice Captain,\n"
                  "PP = Players Played, TM = Transfers Made, H = Hit(s),\n"
                  "TV = Team Value", "Tot = TV + Bank\n"]

        for string in legend:
            log_string(string, self.__output)

    def __print_table_output(self):
        # tabulate requires a list of lists, so that's why it's needed
        list_of_lists = [manager.to_list() for manager in self.__managers]
        headers = self.__init_headers()

        # tablefmt="fancy_grid"
        table_output = tabulate(list_of_lists, headers=headers, tablefmt="orgtbl", floatfmt=".1f", numalign="center",
                                stralign="center")

        log_string(table_output, self.__output)
        log_string("", self.__output)

        formatter = "entry" if len(self.__managers) < 2 else "entries"
        print("\n{} {} have been loaded successfully.".format(len(self.__managers), formatter))
