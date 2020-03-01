from tabulate import tabulate

from analyzers.utility_functions import performance, start_threads
from fileutils.fileutils import log_string, save_output_to_file
from managers.AutosubsManager import AutosubsManager
from parsers.LiveDataParser import LiveDataParser
from parsers.TeamDataParser import TeamDataParser


class AutosubsAnalyzer:
    @performance
    def __init__(self, id_):
        self.__id = id_

        temp_team_data_parser = TeamDataParser(self.__id)
        self.__current_event = temp_team_data_parser.get_current_event()
        self.__manager_name = temp_team_data_parser.get_manager_name()

        self.__managers = self.__init_managers()

        self.__output = []

    def print_table(self):
        self.__print_table_output()
        self.__print_summary()
        self.__print_histogram()

    def save_output_to_file(self):
        path = "output/{}_autosubs_until_gw{}.txt".format(self.__id, self.__current_event)
        save_output_to_file(path, "w", self.__output)

    @start_threads
    def __init_managers(self):
        threads = []
        gw_one = 1

        for i in range(gw_one, self.__current_event + 1):
            live_data_parser = LiveDataParser(i)
            manager = AutosubsManager(self.__id, i, live_data_parser)
            threads.append(manager)

        return threads

    def __sum_bench_points(self):
        used_bench_points = 0
        total_bench_points = 0

        for manager in self.__managers:
            used_bench_points += manager.get_used_bench_points()
            total_bench_points += manager.get_total_bench_points()

        bench_points = [used_bench_points, total_bench_points]
        return bench_points

    def __print_table_output(self):
        log_string("[{}'s Autosubs History:]".format(self.__manager_name), self.__output)
        log_string("", self.__output)

        headers = ["GW",
                   "Players Out", "Players In",
                   "Used BP", "Total BP"]

        # tabulate requires a list of lists, so that's why it's needed
        list_of_lists = [manager.to_list() for manager in self.__managers]

        table_output = tabulate(list_of_lists,
                                headers=headers,
                                tablefmt="orgtbl", floatfmt=".1f",
                                numalign="center", stralign="center")

        log_string(table_output, self.__output)
        log_string("", self.__output)

    def __print_summary(self):
        [used_bench_points, total_bench_points] = self.__sum_bench_points()

        log_string("[Summary:]", self.__output)
        log_string("Used bench points: {}".format(used_bench_points), self.__output)
        log_string("Total bench points: {}".format(total_bench_points), self.__output)
        log_string("", self.__output)

    def __print_histogram(self):
        log_string("[Autosubs Histogram:]", self.__output)
        log_string("", self.__output)

        histogram_headers = ["Name", "Points", "Times"]
        histogram_output = tabulate(self.__managers[0].get_players_in_histogram(),
                                    headers=histogram_headers,
                                    tablefmt="orgtbl",
                                    numalign="center", stralign="center")

        log_string(histogram_output, self.__output)
        self.__output.append("")
