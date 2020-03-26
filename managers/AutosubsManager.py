from functools import cmp_to_key

from managers.Manager import Manager
from parsers.TeamDataParser import TeamDataParser
from parsers.EventDataParser import EventDataParser


class AutosubsManager(Manager):
    players_histogram = {}

    def __init__(self, team_id, current_event, live_data_parser):
        super().__init__(team_id, current_event)
        self.__live_data_parser = live_data_parser

        self.__players_out = self.__players_in = ""
        self.__used_bench_points = self.__total_bench_points = 0

    def run(self):
        self.__init_all_properties()

    def get_used_bench_points(self):
        return self.__used_bench_points

    def get_total_bench_points(self):
        return self.__total_bench_points

    def to_list(self):
        result = [self._current_event,
                  self.__players_out, self.__players_in,
                  self.__used_bench_points, self.__total_bench_points]

        return result

    def get_players_in_histogram(self):
        histogram = self.__players_histogram_to_list()
        histogram.sort(key=cmp_to_key(Player.cmp_points))

        list_of_lists = [player.to_list() for player in histogram]
        return list_of_lists

    def __init_all_properties(self):
        self.__team_data_parser = TeamDataParser(self._id)
        self.__event_data_parser = EventDataParser(self._id, self._current_event)

        self.__init_autosubs()

    def __init_autosubs(self):
        autosubs_ids = self.__event_data_parser.get_autosubs()

        if len(autosubs_ids) == 0:
            self.__players_out = self.__players_in = "None"
            self.__total_bench_points = self.__team_data_parser.get_bench_points_in_specific_gw(self._current_event)

            return

        players_out = []
        players_in = []

        for player_out_id in autosubs_ids:
            player_out = self.__event_data_parser.get_player_name(player_out_id)

            player_in_id = autosubs_ids[player_out_id]
            player_in = self.__event_data_parser.get_player_name(player_in_id)
            player_in_points = self.__live_data_parser.get_player_points(player_in_id)

            self.__add_player_to_histogram(player_in, player_in_points)

            players_out.append(player_out)
            players_in.append("{}:{}".format(player_in, player_in_points))

            self.__used_bench_points += player_in_points

        self.__players_out = ", ".join(players_out)
        self.__players_in = ", ".join(players_in)

        bench_points_in_specific_gw = self.__team_data_parser.get_bench_points_in_specific_gw(self._current_event)
        self.__total_bench_points = self.__used_bench_points + bench_points_in_specific_gw

    def __add_player_to_histogram(self, player_in, player_in_points):
        if player_in in self.players_histogram:
            current_value = self.players_histogram[player_in]
            new_points = current_value[0] + player_in_points
            count = current_value[1] + 1

            self.players_histogram[player_in] = [new_points, count]

        else:
            self.players_histogram[player_in] = [player_in_points, 1]

    def __players_histogram_to_list(self):
        result = []

        for player in self.players_histogram:
            points = self.players_histogram[player][0]
            freq = self.players_histogram[player][1]

            result.append(Player(player, points, freq))

        return result


class Player:
    def __init__(self, name, points, count):
        self.__name = name
        self.__points = points
        self.__count = count

    def to_list(self):
        result = [self.__name, self.__points, self.__count]
        return result

    @staticmethod
    def cmp_points(left, right):
        if left.__points < right.__points:
            return 1
        elif left.__points > right.__points:
            return -1
        else:
            if left.__count < right.__count:
                return -1
            elif left.__count > right.__count:
                return 1
            else:
                return 0
