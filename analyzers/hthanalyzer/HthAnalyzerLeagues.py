import functools

from analyzers.hthanalyzer.HthAnalyzer import HthAnalyzer
from fileutils.FileUtils import FileUtils
from managers.HthManager import HthManager
from parsers.HthParser import HthParser


def pre_matchup_decorator(f):
    @functools.wraps(f)
    def wrapper(self, opponent):
        league = "[League: {}]".format(opponent.league_name)
        FileUtils.log_string(league, self._output)
        f(self, opponent)

    return wrapper


class HthAnalyzerLeagues(HthAnalyzer):
    def __init__(self, team_id):
        super().__init__(team_id=team_id, set_leagues=True)

        self.__cup_opponent_id = self.__get_cup_opponent_id()

        self.__opponents_ids = self._init_opponents_ids()
        self.__average = self.__init_average()

        self.__opponents = self._init_opponents()

    def print_all_matchups(self):
        # [self._print_one_matchup(opponent) for opponent in self.__opponents]
        for opponent in self.__opponents:
            self._print_one_matchup(opponent)

        '''
        def _pre_matchup_decorator(func):
            def inner(self, opponent):
                league = "[League: {}]".format(opponent.league_name)
                FileUtils.log_string(league, self._output)

                func(opponent)

            return inner
        '''

        if len(self.__average) > 0:
            self.__print_average()

        self._print_record()

    @pre_matchup_decorator
    def _print_one_matchup(self, opponent):
        super()._print_one_matchup(opponent)

    def save_output_to_file(self, dummy=""):
        output_file = "output/{}_h2h_matchups_gw{}.txt".format(self._id, self._current_event)
        super().save_output_to_file(output_file)

    def __get_cup_opponent_id(self):
        return self._team.team_data_parser.get_cup_opponent()

    def __print_average(self):
        (my_points, average_points, league_name) = self.__average
        average_data = ["[League: {}]".format(league_name),
                        "[Your score: {}]".format(my_points),
                        "[AVERAGE score: {}".format(average_points)]
        FileUtils.log_list_of_strings(average_data, self._output)

        winner = self._define_winner(self._team.manager_name, my_points, "AVERAGE", average_points)
        winner_string = "[Winner: {}]\n".format(winner)
        FileUtils.log_string(winner_string, self._output)

    def _init_opponents_ids(self):
        print("You're going to see your different players in each H2H match this GW. It'll take a few seconds...\n")

        hth_parser = HthParser(self._id, self._team.leagues, self._current_event)
        opponents_ids = hth_parser.get_opponents_ids()

        return opponents_ids

    def __init_average(self):
        # In a H2H league with odd number of managers,
        # Each GW one of them plays against league's AVERAGE score
        average = ()
        if "AVERAGE" in self.__opponents_ids:
            average = self.__opponents_ids.pop("AVERAGE")

        return average

    def _init_opponents(self):
        threads = []

        if self.__cup_opponent_id != -1:
            self.__cup_opponent = HthManager(self.__cup_opponent_id, self._current_event, False)
            self.__cup_opponent.league_name = "FPL Cup"
            threads.append(self.__cup_opponent)

        # key = opponent's ID
        # value = league's name
        for opponent_id, league_name in self.__opponents_ids.items():
            # set leagues: OFF  -- don't need h2h league codes here
            threads.append(HthManager(opponent_id, self._current_event, False, league_name))

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        return threads
