from abc import ABC, abstractmethod

from analyzers.utility_functions import get_gw_info
from fileutils.fileutils import log_string, log_list_of_strings, save_output_to_file
from managers.HthManager import HthManager
from parsers.LiveDataParser import LiveDataParser


class HthAnalyzer(ABC):
    [_current_event, _, _] = get_gw_info()
    _players_names = {}
    _live_data_parser = LiveDataParser(_current_event)
    _wins = _draws = _losses = 0

    def __init__(self, team_id, set_leagues):
        self._id = team_id

        # Create our manager and start it (because it's a thread)
        self._team = HthManager(self._id, self._current_event, set_leagues)
        self._team.start()
        self._team.join()

        self.__manager_name = self._team.manager_name.split(" ")[0]

        self._output = []

    @abstractmethod
    def print_all_matchups(self):
        pass

    def save_output_to_file(self, output_file):
        save_output_to_file(output_file, "w", self._output)

    def _print_one_matchup(self, opponent):
        ((team_unique_players, team_points), (opp_unique_players, opp_points)) = \
            self._list_of_unique_players_and_their_points(opponent)

        team_manager = self._team.manager_name
        opponent_manager = opponent.manager_name

        unique_players = ["{}: [{}] vs.".format(team_manager, team_unique_players),
                          "{}: [{}]".format(opponent_manager, opp_unique_players)]
        log_list_of_strings(unique_players, self._output)

        if self._team.active_chip != "None" or opponent.active_chip != "None":
            active_chip = ["[Active chip]",
                           "{} vs. {}".format(self._team.active_chip, opponent.active_chip)]
            log_list_of_strings(active_chip, self._output)

        hits_taken = ["[Hits taken]",
                      "{}: {}".format(team_manager, self._team.gw_hits),
                      "{}: {}".format(opponent_manager, opponent.gw_hits)]
        log_list_of_strings(hits_taken, self._output)

        different_players_points = ["[Points gained by different players]",
                                    "{}: {}".format(team_manager, team_points),
                                    "{}: {}".format(opponent_manager, opp_points)]
        log_list_of_strings(different_players_points, self._output)

        if self._team.gw_hits != opponent.gw_hits:
            hit_cost = 4
            team_points -= self._team.gw_hits*hit_cost
            opp_points -= opponent.gw_hits*hit_cost

        # Take hits into account
        self._current_points_difference(team_points, opp_points)

        winner = self._define_winner(team_manager, team_points, opponent_manager, opp_points)
        winner_string = "[Winner: {}]\n".format(winner)
        log_string(winner_string, self._output)

    def _print_record(self):
        record = "[Record: {}W, {}D, {}L]\n".format(self._wins, self._draws, self._losses)
        log_string(record, self._output)

        print("Good luck, {}! :)".format(self.__manager_name))

    def _list_of_unique_players_and_their_points(self, opponent):
        (team_unique_players, team_points) = self._unique_players_and_points(self._team.players_ids,
                                                                             opponent.players_ids,
                                                                             self._team.captain_id)

        (opp_unique_players, opp_points) = self._unique_players_and_points(opponent.players_ids,
                                                                           self._team.players_ids,
                                                                           opponent.captain_id)

        if self._team.captain_id == opponent.captain_id:
            (team_unique_players, points) = self._check_same_captains(self._team, opponent, team_unique_players)
            team_points += points

            (opp_unique_players, points) = self._check_same_captains(opponent, self._team, opp_unique_players)
            opp_points += points

        elif self._team.captain_id != opponent.captain_id:
            (team_unique_players, points) \
                = self._check_different_captains(self._team, team_unique_players, opponent.players_ids)
            team_points += points

            (opp_unique_players, points) = \
                self._check_different_captains(opponent, opp_unique_players, self._team.players_ids)
            opp_points += points

        final_result = ((team_unique_players, team_points), (opp_unique_players, opp_points))

        return final_result

    def __find_different_ids(self, team_a, team_b):
        return team_a.difference(team_b)

    def _unique_players_and_points(self, team_a, team_b, captain_id):
        players_ids = self.__find_different_ids(team_a, team_b)

        def helper():
            result = []
            points = 0

            for player_id in players_ids:
                if player_id == captain_id:
                    continue

                curr_player_points = self._live_data_parser.get_player_points(player_id)

                if player_id in self._players_names:
                    curr_player = "{}={}".format(self._players_names[player_id], curr_player_points)
                    result.append(curr_player)
                else:
                    player_name = self._team.event_data_parser.get_player_name(player_id)
                    self._players_names[player_id] = player_name

                    curr_player = "{}={}".format(player_name, curr_player_points)
                    result.append(curr_player)

                points += curr_player_points

            unique_players = ", ".join(result)
            result = (unique_players, points)

            return result

        return helper()

    def _check_same_captains(self, team_a, team_b, unique_players):
        result = (unique_players, 0)

        if team_a.active_chip == "TC" and team_b.active_chip != "TC":
            captain_points = self._live_data_parser.get_player_points(self._team.captain_id)
            captain_formatted = ", {}={}".format(self._team.captain_name, captain_points)

            unique_players += captain_formatted
            result = (unique_players, captain_points)

        return result

    def _check_different_captains(self, team, unique_players, opponent_players_ids):
        captain_name = team.captain_name
        captain_points = self._live_data_parser.get_player_points(team.captain_id)

        if team.active_chip == "TC":
            if team.captain_id in opponent_players_ids:
                points_to_add = 2*captain_points
                multiplier = "X2"
            else:
                points_to_add = 3*captain_points
                multiplier = "X3"

            captain_name = ", {} {}={}".format(captain_name, multiplier, points_to_add)

        else:
            if team.captain_id in opponent_players_ids:
                points_to_add = captain_points
                captain_name = ", {}={}".format(captain_name, points_to_add)
            else:
                points_to_add = 2*captain_points
                captain_name = ", {} X2={}".format(captain_name, points_to_add)

        unique_players = "{}{}".format(unique_players, captain_name)
        result = (unique_players, points_to_add)

        return result

    def _current_points_difference(self, team_a_points, team_b_points):
        current_result = "trailing" if team_a_points < team_b_points else "leading"
        points_difference = abs(team_a_points - team_b_points)
        formatter = "point" if points_difference == 1 else "points"

        points_difference_string = "You're {} by: {} {}.".format(current_result, abs(team_a_points - team_b_points),
                                                                 formatter)
        log_string(points_difference_string, self._output)

    def _define_winner(self, team_a_manager, team_a_points, team_b_manager, team_b_points):
        if team_a_points > team_b_points:
            self._wins += 1
            return team_a_manager
        elif team_a_points < team_b_points:
            self._losses += 1
            return team_b_manager
        else:
            self._draws += 1
            return "Draw!"

    @abstractmethod
    def _init_opponents_ids(self):
        pass

    @abstractmethod
    def _init_opponents(self):
        pass

