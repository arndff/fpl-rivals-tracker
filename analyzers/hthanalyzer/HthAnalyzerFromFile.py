from analyzers.hthanalyzer.HthAnalyzer import HthAnalyzer
from analyzers.utility_functions import read_ids_from_file, start_threads
from fileutils.fileutils import extract_file_name_from_path
from managers.HthManager import HthManager


class HthAnalyzerFromFile(HthAnalyzer):
    def __init__(self, team_id, ids_file):
        super().__init__(team_id=team_id, set_leagues=False)
        self.__ids_file = ids_file

        self.__opponents_ids = self._init_opponents_ids()
        self.__opponents = self._init_opponents()

    def print_all_matchups(self):
        [self._print_one_matchup(opponent) for opponent in self.__opponents]

        self._print_record()

    def save_output_to_file(self, dummy=""):
        output_file = "output/{}_{}_rivals_comparison_gw{}.txt"
        output_file = output_file.format(self._id,
                                         extract_file_name_from_path(self.__ids_file),
                                         self._current_event)

        super().save_output_to_file(output_file)

    def _init_opponents_ids(self):
        return read_ids_from_file(self.__ids_file, self._id)

    @start_threads
    def _init_opponents(self):
        threads = []

        for opponent_id in self.__opponents_ids:
            threads.append(HthManager(team_id=opponent_id, current_event=self._current_event, set_leagues=False))

        return threads
