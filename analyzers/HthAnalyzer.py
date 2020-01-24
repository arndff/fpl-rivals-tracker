from analyzers.ClassicAnalyzer import ClassicAnalyzer

from fileutils.FileUtils import FileUtils

from managers.Opponent import Opponent

from parsers.HthParser import HthParser
from parsers.LiveDataParser import LiveDataParser
from parsers.TeamDataParser import TeamDataParser


class HthAnalyzer:
    __CURRENT_EVENT = TeamDataParser(1).get_current_event()
    __players_names = {}
    __ldp = LiveDataParser(__CURRENT_EVENT)
    __wins = __draws = __losses = 0

    def __init__(self, id_, default_mode=True, path=""):
        self.__id_ = id_
        self.__default_mode = default_mode
        self.__path = path

        self.__output = []  # A list which stores the whole output

        # Create our manager and start it (because it's a thread)
        if default_mode:
            self.__team = Opponent(id_, self.__CURRENT_EVENT, default_mode)     # set_leagues: ON
        else:
            self.__team = Opponent(id_, self.__CURRENT_EVENT, not default_mode)

        self.__team.start()
        self.__team.join()

        self.__manager_name = self.__team.manager_name.split(" ")[0]

        if default_mode:
            self.__config_default_mode()
        else:
            self.__opponents_ids = ClassicAnalyzer.read_ids_from_file(path, str(id_))

        self.__opponents = self.__init_opponents()

    def save_output_to_file(self):
        # That method may throw exception
        FileUtils.save_hth_output_to_file(self.__path, self.__output,
                                          self.__CURRENT_EVENT, self.__id_,
                                          self.__default_mode)

    def print_all_matchups(self):
        [self.__print_one_matchup(opponent) for opponent in self.__opponents]

        if self.__default_mode and len(self.__average) > 0:
            self.__print_average()

        record = "[Record: {}W, {}D, {}L]\n".format(self.__wins, self.__draws, self.__losses)
        self.__log_string(record)

        print("Good luck, {}! :)".format(self.__manager_name))

    def __print_one_matchup(self, opponent):
        ((team_unique_players, team_points), (opp_unique_players, opp_points)) = \
            self.__list_of_unique_players_and_their_points(opponent)

        team_manager = self.__team.manager_name
        opponent_manager = opponent.manager_name

        if self.__default_mode:
            league = "[League: {}]".format(opponent.league_name)
            self.__log_string(league)

        unique_players = ["{}: [{}] vs.".format(team_manager, team_unique_players),
                          "{}: [{}]".format(opponent_manager, opp_unique_players)]
        self.__handle_output(unique_players)

        if self.__team.active_chip != "None" or opponent.active_chip != "None":
            active_chip = ["[Active chip]",
                           "{} vs. {}".format(self.__team.active_chip, opponent.active_chip)]
            self.__handle_output(active_chip)

        hits_taken = ["[Hits taken]",
                      "{}: {}".format(team_manager, self.__team.gw_hits),
                      "{}: {}".format(opponent_manager, opponent.gw_hits)]
        self.__handle_output(hits_taken)

        different_players_points = ["[Points gained by different players]",
                                    "{}: {}".format(team_manager, team_points),
                                    "{}: {}".format(opponent_manager, opp_points)]
        self.__handle_output(different_players_points)

        if self.__team.gw_hits != opponent.gw_hits:
            hit_cost = 4
            team_points -= self.__team.gw_hits*hit_cost
            opp_points -= opponent.gw_hits*hit_cost

        # Takes hits into account
        self.__current_points_difference(team_points, opp_points)

        winner = self.__define_winner(team_manager, team_points, opponent_manager, opp_points)
        winner_string = "[Winner: {}]\n".format(winner)
        self.__log_string(winner_string)

    def __print_average(self):
        (my_points, average_points, league_name) = self.__average
        average_data = ["[League: {}]".format(league_name),
                        "[Your score: {}]".format(my_points),
                        "[AVERAGE score: {}".format(average_points)]
        self.__handle_output(average_data)

        winner = self.__define_winner(self.__team.manager_name, my_points, "AVERAGE", average_points)
        winner_string = "[Winner: {}]\n".format(winner)
        self.__log_string(winner_string)

    def __list_of_unique_players_and_their_points(self, opponent):
        (team_unique_players, team_points) = self.__unique_players_and_points(self.__team.players_ids,
                                                                              opponent.players_ids,
                                                                              self.__team.captain_id)

        (opp_unique_players, opp_points) = self.__unique_players_and_points(opponent.players_ids,
                                                                            self.__team.players_ids,
                                                                            opponent.captain_id)

        if self.__team.captain_id == opponent.captain_id:
            (team_unique_players, points) = self.__check_same_captains(self.__team, opponent, team_unique_players)
            team_points += points

            (opp_unique_players, points) = self.__check_same_captains(opponent, self.__team, opp_unique_players)
            opp_points += points

        elif self.__team.captain_id != opponent.captain_id:
            (team_unique_players, points) \
                = self.__check_different_captains(self.__team, team_unique_players, opponent.players_ids)
            team_points += points

            (opp_unique_players, points) = \
                self.__check_different_captains(opponent, opp_unique_players, self.__team.players_ids)
            opp_points += points

        final_result = ((team_unique_players, team_points), (opp_unique_players, opp_points))

        return final_result

    @staticmethod
    def __find_different_ids(team_a, team_b):
        return team_a.difference(team_b)

    def __unique_players_and_points(self, team_a, team_b, captain_id):
        players_ids = self.__find_different_ids(team_a, team_b)

        def helper():
            result = []
            points = 0

            for player_id in players_ids:
                if player_id == captain_id:
                    continue

                curr_player_points = self.__ldp.get_player_points(player_id)

                if player_id in self.__players_names:
                    curr_player = "{}={}".format(self.__players_names[player_id], curr_player_points)
                    result.append(curr_player)
                else:
                    player_name = self.__team.event_data_parser.get_player_name(player_id)
                    self.__players_names[player_id] = player_name

                    curr_player = "{}={}".format(player_name, curr_player_points)
                    result.append(curr_player)

                points += curr_player_points

            unique_players = ", ".join(result)
            result = (unique_players, points)

            return result

        return helper()

    def __check_same_captains(self, team_a, team_b, unique_players):
        result = (unique_players, 0)

        if team_a.active_chip == "TC" and team_b.active_chip != "TC":
            captain_points = self.__ldp.get_player_points(self.__team.captain_id)
            captain_formatted = ", {}={}".format(self.__team.captain_name, captain_points)

            unique_players += captain_formatted
            result = (unique_players, captain_points)

        return result

    def __check_different_captains(self, team, unique_players, opponent_players_ids):
        captain_name = team.captain_name
        captain_points = self.__ldp.get_player_points(team.captain_id)

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

    def __current_points_difference(self, team_a_points, team_b_points):
        current_result = "trailing" if team_a_points < team_b_points else "leading"
        points_difference = abs(team_a_points - team_b_points)
        formatter = "point" if points_difference == 1 else "points"

        points_difference_string = "You're {} by: {} {}.".format(current_result, abs(team_a_points - team_b_points), formatter)
        self.__log_string(points_difference_string)

    def __define_winner(self, team_a_manager, team_a_points, team_b_manager, team_b_points):
        if team_a_points > team_b_points:
            self.__wins += 1
            return team_a_manager
        elif team_a_points < team_b_points:
            self.__losses += 1
            return team_b_manager
        else:
            self.__draws += 1
            return "Draw!"

    def __init_opponents(self):
        threads = []

        if self.__default_mode:
            if self.__cup_opponent_id != -1:
                self.__cup_opponent = Opponent(self.__cup_opponent_id, self.__CURRENT_EVENT, False)
                self.__cup_opponent.league_name = "FPL Cup"
                threads.append(self.__cup_opponent)

            # key = opponent's ID
            # value = league's name
            for opponent_id, league_name in self.__opponents_ids.items():
                # set leagues: OFF  -- don't need h2h league codes here
                threads.append(Opponent(opponent_id, self.__CURRENT_EVENT, False, league_name))

        else:
            for opponent_id in self.__opponents_ids:
                threads.append(Opponent(opponent_id, self.__CURRENT_EVENT, False))

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        return threads

    def __config_default_mode(self):
        self.__cup_opponent_id = self.__team.team_data_parser.get_cup_opponent()
        # self.__cup_opponent_id = -1

        hth_parser = HthParser(self.__id_, self.__team.leagues, self.__CURRENT_EVENT)

        print("You're going to see your different players in each H2H match this GW. It'll take a few seconds...\n")

        self.__opponents_ids = hth_parser.get_opponents_ids()

        self.__average = ()

        # In a H2H league with odd number of managers,
        # Each GW one of them plays against league's AVERAGE score
        if "AVERAGE" in self.__opponents_ids:
            self.__average = self.__opponents_ids.pop("AVERAGE")

    def __log_string(self, string):
        print(string)
        self.__output.append(string)

    def __handle_output(self, array):
        for string in array:
            print(string)
            self.__output.append(string)
