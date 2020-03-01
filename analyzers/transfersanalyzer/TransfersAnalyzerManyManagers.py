from functools import cmp_to_key
from tabulate import tabulate

from analyzers.transfersanalyzer.TransfersAnalyzer import TransfersAnalyzer
from analyzers.utility_functions import read_ids, set_output_file, performance, start_threads
from fileutils.fileutils import extract_file_name_from_path, log_string, save_output_to_file
from managers.TransfersManager import TransfersManager
from parsers.LiveDataParser import LiveDataParser


class TransfersAnalyzerManyManagers(TransfersAnalyzer):
    @performance
    def __init__(self, ids_file, league_name="", league_id=-1, managers_count=-1):
        self.__ids_file = ids_file
        self.__league_name = league_name

        self.__ids = read_ids(ids_file, league_id, managers_count)
        self.__managers = self._init_managers()

        self.__output = []
        self.__output_file = set_output_file(self._current_event, "transfers", ids_file, league_name, league_id)

    def save_output_to_file(self):
        if self.__ids_file != "":
            output_file_prefix = extract_file_name_from_path(self.__ids_file)
        else:
            output_file_prefix = self.__league_name

        output_file = "output/{}_transfers_gw{}.txt".format(output_file_prefix, self._current_event)
        save_output_to_file(output_file, "w", self.__output)

    # prints a couple of managers' transfers in a during GW
    def print_table(self):
        self.__sort_managers()
        self.__format_managers_outcome()

        self.__print_legend()
        self._print_table_output()

        self._print_wc_fh_info()

        formatter = "entry" if len(self.__managers) < 2 else "entries"
        print("{} {} have been loaded successfully.".format(len(self.__managers), formatter))

    @start_threads
    def _init_managers(self):
        live_data_parser = LiveDataParser(self._current_event)
        threads = list(map(lambda id_: TransfersManager(id_, self._current_event, live_data_parser), self.__ids))
        return threads

    def __sort_managers(self):
        self.__managers.sort(key=cmp_to_key(TransfersManager.cmp_gw_outcome))

    def __format_managers_outcome(self):
        row_num = 1
        for manager in self.__managers:
            manager.format_outcome()

            manager.row_num = row_num
            row_num += 1

    def __print_legend(self):
        legend = ["[Legend:]",
                  "TM = Transfers Made, H = Hit(s),",
                  "Outcome: Points gained/lost from transfers,",
                  "TV = Team Value,", "Tot = TV + Bank\n"]

        for string in legend:
            log_string(string, self.__output)

    def _print_table_output(self):
        log_string(self._WC_MSG, self.__output)

        list_of_lists = [manager.to_list() for manager in self.__managers]
        headers = ["No", "Manager",
                   "Transfers Out", "Transfers In",
                   "{} TM".format(self._gw_name), "{} H".format(self._gw_name),
                   "Outcome", "{} P".format(self._gw_name),
                   "TV", "Bank", "Tot"]

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
