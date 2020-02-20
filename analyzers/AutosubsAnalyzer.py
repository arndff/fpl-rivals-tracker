import time

from tabulate import tabulate

from fileutils.FileUtils import FileUtils

from managers.AutosubsManager import AutosubsManager

from parsers.LiveDataParser import LiveDataParser
from parsers.TeamDataParser import TeamDataParser


class AutosubsAnalyzer:
    def __init__(self, id_):
        self.__id_ = id_

        start_time = time.time()

        # Create an object from TeamDataParser class to get current gw's number
        temp_team_data_parser = TeamDataParser(id_)
        self.__current_event = temp_team_data_parser.get_current_event()

        self.__managers = self.__init_managers()

        self.__output = []

        execution_time = time.time() - start_time
        print("Data was collected for {:.2f} seconds\n".format(execution_time))

        FileUtils.log_string("[{}'s Autosubs History:]".format(temp_team_data_parser.get_manager_name()), self.__output)
        FileUtils.log_string("", self.__output)

    def print_table(self):
        headers = ["GW",
                   "Players Out", "Players In",
                   "Used BP", "Total BP"]

        used_bench_points = 0
        total_bench_points = 0

        for manager in self.__managers:
            used_bench_points += manager.get_used_bench_points()
            total_bench_points += manager.get_total_bench_points()

        # tabulate requires a list of lists, so that's why it's needed
        list_of_lists = [manager.to_list() for manager in self.__managers]

        table_output = tabulate(list_of_lists,
                                headers=headers,
                                tablefmt="orgtbl", floatfmt=".1f",
                                numalign="center", stralign="center")

        FileUtils.log_string(table_output, self.__output)
        FileUtils.log_string("", self.__output)
        FileUtils.log_string("[Summary:]", self.__output)
        FileUtils.log_string("Used bench points: {}".format(used_bench_points), self.__output)
        FileUtils.log_string("Total bench points: {}".format(total_bench_points), self.__output)
        FileUtils.log_string("", self.__output)

        FileUtils.log_string("[Autosubs Histogram:]", self.__output)
        FileUtils.log_string("", self.__output)

        histogram_headers = ["Name", "Points", "Times"]
        histogram_output = tabulate(self.__managers[0].get_players_in_histogram(),
                                    headers=histogram_headers,
                                    tablefmt="orgtbl",
                                    numalign="center", stralign="center")

        FileUtils.log_string(histogram_output, self.__output)
        self.__output.append("")

    def save_output_to_file(self):
        path = "output/{}_autosubs_until_gw{}.txt".format(self.__id_, self.__current_event)
        FileUtils.save_output_to_file(path, "w", self.__output)

    def __init_managers(self):
        threads = []
        gw_one = 1

        for i in range(gw_one, self.__current_event + 1):
            live_data_parser = LiveDataParser(i)
            manager = AutosubsManager(self.__id_, i, live_data_parser)
            threads.append(manager)

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        return threads
