import time

from operator import methodcaller
from tabulate import tabulate

from managers.Rival import Rival
from menus.RivalsMenu import RivalsMenu

from parsers.LiveDataParser import LiveDataParser
from parsers.TeamDataParser import TeamDataParser


class ClassicAnalyzer:
    __LAST_EVENT = 38

    def __init__(self, path):
        start_time = time.time()

        self.__ids = ClassicAnalyzer.read_ids_from_file(path)

        # Create an object from TeamDataParser class to get current gw's number
        tmp_obj = TeamDataParser(1)
        self.__curr_event = tmp_obj.get_current_event()
        self.__is_dgw = self.__curr_event in tmp_obj.DGW
        self.__ldp = LiveDataParser(self.__curr_event, self.__is_dgw)

        self.__managers = self.__init_managers()
        self.__init_each_manager_players_played()

        if self.__is_dgw:
            self.__init_each_manager_dgw_players_count()

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

        headers = ["No", "Manager", "OR", "OP", "Used Chips",
                   "GW{} P".format(self.__curr_event),
                   "GW{} C".format(self.__curr_event),
                   "GW{} VC".format(self.__curr_event),
                   "GW{} Chip".format(self.__curr_event),
                   "Players Played",
                   "GW{} TM".format(next_event),
                   "GW{} H".format(next_event),
                   "TV", "Bank"]

        if self.__is_dgw:
            headers.insert(10, "DGW Players")

        print("\n> Legend: ")
        print("OR = Overall Rank, OP = Overall Points, P = Points, C = Captain, VC = Vice Captain, "
              "TM = Transfers Made, H = Hit(s), TV = Team Value\n")

        print(tabulate(list_of_lists,
                       headers=headers,
                       tablefmt="orgtbl", floatfmt=".1f",
                       numalign="center", stralign="center"))

        formatter = "entry" if len(self.__managers) < 2 else "entries"
        print("\n{} {} were loaded successfully.".format(len(self.__managers), formatter))

    def print_stats(self):
        rivals_menu = RivalsMenu(self.__managers, self.__curr_event)
        rivals_menu.stats_menu()

    @staticmethod
    def read_ids_from_file(path, my_id=-1):
        with open(path, "r") as input_file:
            lines = input_file.readlines()
            ids = {line.rstrip('\n') for line in lines}

            """
            this is used in HthAnalyzer class when you want to compare your team to some others
            the point is to remove your id (if it exists) from the given file with ids
            because it's pointless to compare your team to itself 
            """
            ids.discard(my_id)

        return ids

    def __init_managers(self):
        threads = list(map(lambda id_: Rival(id_, self.__curr_event, self.__is_dgw), self.__ids))

        """
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        """

        [thread.start() for thread in threads]

        [thread.join() for thread in threads]

        return threads

    def __init_each_manager_players_played(self):
        for manager in self.__managers:
            players_played = self.__ldp.count_players_played(manager.players_ids)
            manager.format_players_played(players_played)

    def __init_each_manager_dgw_players_count(self):
        for manager in self.__managers:
            dgw_players_count = self.__ldp.get_dgw_players_count(manager.players_ids)
            manager.dgw_players_count = dgw_players_count

    def __calc_next_event(self):
        if self.__curr_event != self.__LAST_EVENT:
            return self.__curr_event + 1
        else:
            return self.__curr_event
