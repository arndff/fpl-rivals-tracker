from parsers.TeamDataParser import TeamDataParser
from parsers.LiveDataParser import LiveDataParser

from rivals.Manager import Manager
from menus.RivalsMenu import RivalsMenu

from operator import methodcaller
from tabulate import tabulate

import time


class Analyzer:
    def __init__(self, path):
        start_time = time.time()

        with open(path, "r") as input_file:
            lines = input_file.readlines()
            self.__ids = [line.rstrip('\n') for line in lines]

        # Create an object from TeamDataParser class to get current gw's number
        tmp_obj = TeamDataParser(1)
        self.__curr_event = tmp_obj.get_current_event()

        self.__managers = self.__init_managers()
        self.__init_each_manager_players_played()

        execution_time = time.time() - start_time
        print("Data was collected for {:.2f} seconds".format(execution_time))

    def print_table(self):
        """
        menu returns an integer which indicates how the data is going to be sorted
        1: by total points
        2: by gameweek points
        """
        comparator = RivalsMenu.menu()

        # sort the data
        if comparator[0] == 1:
            self.__managers.sort(key=methodcaller(comparator[1]), reverse=False)
        else:
            self.__managers.sort(key=methodcaller(comparator[1]), reverse=True)

        row_num = 1

        # format some of its columns
        for manager in self.__managers:
            manager.format_total_points_and_overall_rank()
            manager.format_gw_points()

            manager.row_num = row_num
            row_num += 1

        # tabulate requires a list of lists, so that's why it's needed
        list_of_lists = [manager.to_list() for manager in self.__managers]
        next_event = self.__calc_next_event()

        headers = ["No", "Manager", "OR", "Points", "Used Chips",
                   "GW{} Points".format(self.__curr_event),
                   "GW{} C".format(self.__curr_event),
                   "GW{} VC".format(self.__curr_event),
                   "GW{} Chip".format(self.__curr_event),
                   "Players Played",
                   "GW{} Transfers".format(next_event),
                   "GW{} Hits".format(next_event),
                   "Squad Value", "Bank"]

        print(tabulate(list_of_lists,
                       headers=headers,
                       tablefmt="orgtbl", floatfmt=".1f",
                       numalign="center", stralign="center"))

        formatter = "entry" if len(self.__managers) < 2 else "entries"
        print("\n{} {} were loaded successfully.".format(len(self.__managers), formatter))

    def print_stats(self):
        rivals_menu = RivalsMenu(self.__managers, self.__curr_event)
        rivals_menu.stats_menu()

    def __init_managers(self):
        threads = list(map(lambda id_: Manager(id_, self.__curr_event), self.__ids))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return threads

    def __init_each_manager_players_played(self):
        ldp = LiveDataParser(self.__curr_event)

        for manager in self.__managers:
            players_played = ldp.count_players_played(manager.players_ids)
            manager.format_players_played(players_played)

    def __calc_next_event(self):
        last_event = 38

        if self.__curr_event != last_event:
            return self.__curr_event + 1
        else:
            return self.__curr_event
