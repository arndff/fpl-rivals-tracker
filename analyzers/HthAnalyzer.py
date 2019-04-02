from analyzers.ClassicAnalyzer import ClassicAnalyzer

from managers.Opponent import Opponent

from parsers.HthParser import HthParser
from parsers.LiveDataParser import LiveDataParser
from parsers.TeamDataParser import TeamDataParser


class HthAnalyzer:
    __CURR_EVENT = TeamDataParser(1).get_current_event()
    __players_names = {}
    __ldp = LiveDataParser(__CURR_EVENT)
    __wins = __draws = __losses = 0

    def __init__(self, id_, default_mode=True, path=""):
        # Create our manager and start it (because it's a thread)
        self.__id_ = id_
        self.__default_mode = default_mode

        if default_mode:
            self.__team = Opponent(id_, self.__CURR_EVENT, default_mode)  # set_leagues: ON
        else:
            self.__team = Opponent(id_, self.__CURR_EVENT, not default_mode)

        self.__team.start()
        self.__team.join()

        self.manager_name = self.__team.manager_name.split(" ")[0]

        if default_mode:
            self.__cup_opponent_id = self.__team.tdp.get_cup_opponent()

            hth_parser = HthParser(self.__id_, self.__team.leagues)
            self.__opponents_ids = hth_parser.get_opponents_ids()

        else:
            self.__opponents_ids = ClassicAnalyzer.read_ids_from_file(path, str(id_))

        self.__opponents = self.__init_opponents()

    def __init_opponents(self):
        threads = []

        if self.__default_mode:
            if self.__cup_opponent_id != -1:
                self.__cup_opponent = Opponent(self.__cup_opponent_id, self.__CURR_EVENT, False)
                self.__cup_opponent.league_name = "FPL Cup"
                threads.append(self.__cup_opponent)

            # key = opponent's ID
            # value = league's name
            for opponent_id, league_name in self.__opponents_ids.items():
                # set leagues: OFF  -- don't need h2h league codes here
                threads.append(Opponent(opponent_id, self.__CURR_EVENT, False, league_name))

        else:
            for opponent_id in self.__opponents_ids:
                threads.append(Opponent(opponent_id, self.__CURR_EVENT, False))

        """
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        """

        [thread.start() for thread in threads]

        [thread.join() for thread in threads]

        return threads

    @staticmethod
    def __find_different_ids(team_a, team_b):
        return team_a.difference(team_b)

    def __list_of_unique_players_and_their_points(self, team_a, team_b, captain_id):
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
                    player_name = self.__team.edp.get_player_name(player_id)
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

    def __check_different_captains(self, team, unique_players):
        captain_name = team.captain_name
        captain_points = self.__ldp.get_player_points(team.captain_id)

        if team.active_chip == "TC":
            points_to_add = 3*captain_points
            captain_name = "{} X3=".format(captain_name, points_to_add)
        else:
            points_to_add = 2*captain_points
            captain_name = ", {} X2={}".format(captain_name, points_to_add)

        unique_players = "{}{}".format(unique_players, captain_name)
        result = (unique_players, points_to_add)

        return result

    # there's a temporary variable called "result" which stores a single tuple
    def __unique_players_and_their_points(self, opponent):
        result = self.__list_of_unique_players_and_their_points(self.__team.players_ids,
                                                                opponent.players_ids,
                                                                self.__team.captain_id)

        team_unique_players = result[0]
        team_points = result[1]

        result = self.__list_of_unique_players_and_their_points(opponent.players_ids,
                                                                self.__team.players_ids,
                                                                opponent.captain_id)

        opp_unique_players = result[0]
        opp_points = result[1]

        if self.__team.captain_id == opponent.captain_id:
            result = self.__check_same_captains(self.__team, opponent, team_unique_players)
            team_unique_players = result[0]
            team_points += result[1]

            result = self.__check_same_captains(opponent, self.__team, opp_unique_players)
            opp_unique_players = result[0]
            opp_points += result[1]

        elif self.__team.captain_id != opponent.captain_id:
            result = self.__check_different_captains(self.__team, team_unique_players)
            team_unique_players = result[0]
            team_points += result[1]

            result = self.__check_different_captains(opponent, opp_unique_players)
            opp_unique_players = result[0]
            opp_points += result[1]

        final_result = ((team_unique_players, team_points), (opp_unique_players, opp_points))

        return final_result

    @staticmethod
    def __current_points_difference(team_a_points, team_b_points):
        if team_a_points < team_b_points:
            print("You're trailing by: {} points.".format(team_b_points - team_a_points))
        elif team_a_points > team_b_points:
            print("You're leading by: {} points.".format(team_a_points - team_b_points))

    def __current_winner(self, team_a_manager, team_a_points, team_b_manager, team_b_points):
        if team_a_points > team_b_points:
            self.__wins += 1
            return team_a_manager
        elif team_a_points < team_b_points:
            self.__losses += 1
            return team_b_manager
        else:
            self.__draws += 1
            return "Draw!"

    def __print_one_matchup(self, opponent):
        unique_players_and_points = self.__unique_players_and_their_points(opponent)

        team_manager = self.__team.manager_name
        opponent_manager = opponent.manager_name

        if self.__default_mode:
            print("[League: {}]".format(opponent.league_name))

        print("{}: [{}] vs.".format(team_manager, unique_players_and_points[0][0]))
        print("{}: [{}]".format(opponent_manager, unique_players_and_points[1][0]))

        if self.__team.active_chip != "None" or opponent.active_chip != "None":
            print("[Active chip]")
            print("{} vs. {}".format(self.__team.active_chip, opponent.active_chip))

        team_points = unique_players_and_points[0][1]
        opp_points = unique_players_and_points[1][1]

        print("[Points gained by different players]")
        print("{}: {}".format(team_manager, team_points))
        print("{}: {}".format(opponent_manager, opp_points))

        self.__current_points_difference(team_points, opp_points)

        current_winner = self.__current_winner(team_manager, team_points, opponent_manager, opp_points)
        print("[Current winner: {}]".format(current_winner))

        print()

    def print_all_matchups(self):
        [self.__print_one_matchup(opponent) for opponent in self.__opponents]
        print("[Record: {}W, {}D, {}L]\n".format(self.__wins, self.__draws, self.__losses))
