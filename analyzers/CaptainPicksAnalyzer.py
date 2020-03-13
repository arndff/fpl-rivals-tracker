from collections import OrderedDict
from tabulate import tabulate

from analyzers.utility_functions import get_current_event, performance, start_threads
from managers.ClassicManager import ClassicManager
from parsers.LiveDataParser import LiveDataParser


class CaptainPickAnalyzer:
    @performance
    def __init__(self, team_id):
        self.__id = team_id
        self.__current_event = get_current_event()

        self.__live_data_parsers = []
        self.__managers = self.__init_managers()
        self.__manager_name = self.__get_manager_name()

        self.__if_swapped_points = []

    def print_table(self):
        list_of_lists = self.__managers_to_list_of_lists()
        self.__print_table_output(list_of_lists)
        self.__print_summary(list_of_lists)

    @start_threads
    def __init_managers(self):
        threads = []
        gw = 1

        for i in range(gw, self.__current_event + 1):
            live_data_parser = LiveDataParser(i)
            self.__live_data_parsers.append(live_data_parser)

            threads.append(ClassicManager(team_id=self.__id,
                                          current_event=i,
                                          is_dgw=False,
                                          live_data_parser=live_data_parser))

        return threads

    def __get_manager_name(self):
        return self.__managers[0].manager_name

    def __print_table_output(self, list_of_lists):
        print("[{}'s Captain Picks Analysis:]\n".format(self.__manager_name))
        headers = ["GW", "C Name", "C Points", "VC Name", "VC Points"]
        # tablefmt="fancy_grid"
        table_output = tabulate(list_of_lists, headers=headers, tablefmt="orgtbl", floatfmt=".1f", numalign="center",
                                stralign="center")
        print(table_output)

    def __managers_to_list_of_lists(self):
        list_of_lists = []
        gw = 1

        for i in range(gw - 1, self.__current_event):
            current_manager = self.__manager_to_list(self.__managers[i], i)
            self.__if_swapped_points.append(current_manager.pop())
            list_of_lists.append(current_manager)

        return list_of_lists

    def __manager_to_list(self, manager, index):
        row = index + 1
        live_data_parser = self.__live_data_parsers[index]
        autosubbed_captain = [False]  # wrapping a bool var into list

        captains_data = self.__get_captains_data(manager, live_data_parser, autosubbed_captain)
        [captain_name, vice_captain_name] = [captains_data[0][0], captains_data[1][0]]
        [captain_points, vice_captain_points] = [captains_data[0][1], captains_data[1][1]]

        captain_points *= 2
        if manager.active_chip == "TC":
            captain_points += int(captain_points / 2)
            row = "TC"

        # C played, VC played or both didn't play
        if not autosubbed_captain[0]:
            if_swapped = 2*vice_captain_points
            if manager.active_chip == "TC":
                if_swapped += int(if_swapped/2)
        # C played, VC didn't or the opposite happened
        else:
            if_swapped = captain_points
            if manager.active_chip == "TC":
                if_swapped += captain_points

        result = [row, captain_name, captain_points, vice_captain_name, vice_captain_points, if_swapped]
        return result

    def __get_captains_data(self, manager, live_data_parser, autosubbed_captain):
        [captain_id, captain_name] = [manager.captain_id, manager.captain_name]
        [vice_captain_id, vice_captain_name] = [manager.vice_captain_id, manager.vice_captain_name]
        captain_points = live_data_parser.get_player_points(captain_id)
        vice_captain_points = live_data_parser.get_player_points(vice_captain_id)

        captains_data = OrderedDict()
        captains_data[captain_name] = captain_points
        captains_data[vice_captain_name] = vice_captain_points

        autosubs = manager.event_data_parser.get_autosubs()

        # need to know this in order to calculate if_swapped correctly
        if captain_id in autosubs or vice_captain_id in autosubs:
            autosubbed_captain[0] = True

        # if the captained player did NOT play
        # then we reverse captain_data (C -> VC)
        if captain_id in autosubs:
            captains_data_reversed = OrderedDict()
            for key in reversed(captains_data):
                captains_data_reversed[key] = captains_data[key]

            return list(captains_data_reversed.items())

        return list(captains_data.items())

    def __print_summary(self, list_of_lists):
        total_captain_points = total_vice_captain_points = 0

        captain_points_index = 2
        vice_captain_points_index = 4

        if_swapped_points = 0

        length = len(list_of_lists)
        for i in range(0, length):
            total_captain_points += list_of_lists[i][captain_points_index]
            total_vice_captain_points += list_of_lists[i][vice_captain_points_index]
            if_swapped_points += self.__if_swapped_points[i]

        print("\n[Summary:]")
        print("Total C points: {}".format(total_captain_points))
        print("Total VC points: {}".format(total_vice_captain_points))
        print("If swapped: {}\n".format(if_swapped_points))
        print("(C points) - (If swapped): {}".format(total_captain_points - if_swapped_points))
