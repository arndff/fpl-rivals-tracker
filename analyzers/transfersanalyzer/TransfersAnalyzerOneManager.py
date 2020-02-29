import time

from functools import reduce
from tabulate import tabulate

from analyzers.transfersanalyzer.TransfersAnalyzer import TransfersAnalyzer
from fileutils.FileUtils import FileUtils
from managers.TransfersManager import TransfersManager
from parsers.LiveDataParser import LiveDataParser


class TransfersAnalyzerOneManager(TransfersAnalyzer):
    def __init__(self, team_id):
        super()
        self.__id_ = team_id

        start_time = time.time()

        self.__managers = self._init_managers()
        [self.__transfers_made, self.__hits_taken, self.__total_outcome] = [0, 0, 0]

        self.__output = []

        execution_time = time.time() - start_time
        print("Data was collected for {:.2f} seconds\n".format(execution_time))

    def save_output_to_file(self):
        output_file = "output/{}_transfers_until_gw{}.txt".format(self.__id_, self._current_event)
        FileUtils.save_output_to_file(output_file, "w", self.__output)

    # prints all transfers of one manager during the whole season
    def print_table(self):
        self.__init_stats()
        self.__format_managers_outcome()

        self._print_table_output()
        self._print_wc_fh_info()
        self.__print_summary()

    def _init_managers(self):
        threads = []
        gw_one = 1

        for i in range(gw_one, self._current_event + 1):
            live_data_parser = LiveDataParser(i)
            manager = TransfersManager(self.__id_, i, live_data_parser)
            threads.append(manager)

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        return threads

    def __format_managers_outcome(self):
        [manager.format_outcome() for manager in self.__managers]

    def __init_stats(self):
        def do_sum(x, y):
            return x + y

        self.__transfers_made = reduce(do_sum, list(map(lambda x: x.gw_transfers, self.__managers)), 0)
        self.__hits_taken = reduce(do_sum, list(map(lambda x: x.gw_hits, self.__managers)), 0)
        self.__total_outcome = reduce(do_sum, list(map(lambda x: x.outcome, self.__managers)), 0)

    def _print_table_output(self):
        FileUtils.log_string(self._WC_MSG, self.__output)

        headers = ["GW", "OR", "Transfers Out", "Transfers In", "Transfers Made", "Hits", "Outcome"]
        list_of_lists = [manager.to_list_gw() for manager in self.__managers]

        table_output = tabulate(list_of_lists,
                                headers=headers,
                                tablefmt="orgtbl", floatfmt=".1f",
                                numalign="center", stralign="center")

        FileUtils.log_string(table_output, self.__output)
        FileUtils.log_string("", self.__output)

    def _print_wc_fh_info(self):
        for manager in self.__managers:
            if manager.get_wc_info() is not None:
                info = manager.get_wc_info()
                FileUtils.log_string(info, self.__output)
                FileUtils.log_string("", self.__output)

    def __print_summary(self):
        FileUtils.log_string("[Summary:]", self.__output)
        FileUtils.log_string("Transfers made: {}".format(self.__transfers_made), self.__output)
        FileUtils.log_string("Hits taken: {}".format(self.__hits_taken), self.__output)

        sign = ""
        if self.__total_outcome > 0:
            sign = "+"

        FileUtils.log_string("Total outcome: {}{}".format(sign, self.__total_outcome), self.__output)
        self.__output.append("")
