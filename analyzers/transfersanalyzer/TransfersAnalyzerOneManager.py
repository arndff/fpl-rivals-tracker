from functools import reduce
from tabulate import tabulate

from analyzers.transfersanalyzer.TransfersAnalyzer import TransfersAnalyzer
from analyzers.utility_functions import performance, start_threads
from fileutils.fileutils import log_string, save_output_to_file
from managers.TransfersManager import TransfersManager
from parsers.LiveDataParser import LiveDataParser


class TransfersAnalyzerOneManager(TransfersAnalyzer):
    @performance
    def __init__(self, team_id):
        super()
        self.__id_ = team_id

        self.__managers = self._init_managers()
        [self.__transfers_made, self.__hits_taken, self.__total_outcome] = [0, 0, 0]

        self.__output = []

    def save_output_to_file(self):
        output_file = "output/{}_transfers_until_gw{}.txt".format(self.__id_, self._current_event)
        save_output_to_file(output_file, "w", self.__output)

    # prints all transfers of one manager during the whole season
    def print_table(self):
        self.__init_stats()
        self.__format_managers_outcome()

        self._print_table_output()
        self._print_wc_fh_info()
        self.__print_summary()

    @start_threads
    def _init_managers(self):
        threads = []
        gw_one = 1

        for i in range(gw_one, self._current_event + 1):
            live_data_parser = LiveDataParser(i)
            manager = TransfersManager(self.__id_, i, live_data_parser)
            threads.append(manager)

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
        log_string(self._WC_MSG, self.__output)

        headers = ["GW", "OR", "Transfers Out", "Transfers In", "Transfers Made", "Hits", "Outcome"]
        list_of_lists = [manager.to_list_gw() for manager in self.__managers]

        table_output = tabulate(list_of_lists,
                                headers=headers,
                                tablefmt="orgtbl", floatfmt=".1f",
                                numalign="center", stralign="center")

        log_string(table_output, self.__output)
        log_string("", self.__output)

    def _print_wc_fh_info(self):
        for manager in self.__managers:
            if manager.get_wc_info() is not None:
                info = manager.get_wc_info()
                log_string(info, self.__output)
                log_string("", self.__output)

    def __print_summary(self):
        log_string("[Summary:]", self.__output)
        log_string("Transfers made: {}".format(self.__transfers_made), self.__output)
        log_string("Hits taken: {}".format(self.__hits_taken), self.__output)

        sign = ""
        if self.__total_outcome > 0:
            sign = "+"

        log_string("Total outcome: {}{}".format(sign, self.__total_outcome), self.__output)
        self.__output.append("")
