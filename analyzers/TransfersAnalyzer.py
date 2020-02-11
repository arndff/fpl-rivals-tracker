import time

from functools import cmp_to_key, reduce
from tabulate import tabulate

from analyzers.ClassicAnalyzer import ClassicAnalyzer
from fileutils.FileUtils import FileUtils
from managers.TransfersManager import TransfersManager
from parsers.TeamDataParser import TeamDataParser
from parsers.LiveDataParser import LiveDataParser


class TransfersAnalyzer:
    def __init__(self, path="", id_=-1):
        self.__path = path
        self.__id_ = id_

        start_time = time.time()

        # Create an object from TeamDataParser class to get current gw's number
        temp_team_data_parser = TeamDataParser(1)
        self.__current_event = temp_team_data_parser.get_current_event()
        self.__gw_name = temp_team_data_parser.get_gw_name(self.__current_event)

        if self.__path != "":
            self.__ids = ClassicAnalyzer.read_ids_from_file(path)

        self.__managers = self.__init_managers()

        self.__WC_MSG = "[WC outcome:] (Transfers IN - Transfers OUT) [incl. bench points]\n"
        self.__output = []

        execution_time = time.time() - start_time
        print("Data was collected for {:.2f} seconds\n".format(execution_time))

    def save_output_to_file(self):
        if self.__path == "":
            new_path = "output/{}_transfers_until_gw{}.txt.txt".format(self.__id_, self.__current_event)
        else:
            new_path = "output/{}_transfers_gw{}.txt".format(FileUtils.extract_file_name_from_path(self.__path),
                                                             self.__current_event)

        FileUtils.save_output_to_file(new_path, "w", self.__output)

    # prints all transfers of one manager during the whole season
    def print_all_transfers(self):
        self.__log_string(self.__WC_MSG)
        headers = ["GW", "OR", "Transfers Out", "Transfers In", "Transfers Made", "Hits", "Outcome"]

        def do_sum(x, y):
            return x + y

        transfers_made = reduce(do_sum, list(map(lambda x: x.gw_transfers, self.__managers)), 0)
        hits_taken = reduce(do_sum, list(map(lambda x: x.gw_hits, self.__managers)), 0)
        total_outcome = reduce(do_sum, list(map(lambda x: x.outcome, self.__managers)), 0)

        [manager.format_outcome() for manager in self.__managers]

        wc_fh_info = []
        list_of_lists = []
        for manager in self.__managers:
            list_of_lists.append(manager.to_list_gw())

            if manager.get_wc_info() is not None:
                wc_fh_info.append(manager.get_wc_info())

        table_output = tabulate(list_of_lists,
                                headers=headers,
                                tablefmt="orgtbl", floatfmt=".1f",
                                numalign="center", stralign="center")

        self.__log_string(table_output)
        self.__log_string("")

        for entry in wc_fh_info:
            self.__log_string(entry)
            self.__log_string("")

        self.__log_string("[Summary:]")
        self.__log_string("Transfers made: {}".format(transfers_made))
        self.__log_string("Hits taken: {}".format(hits_taken))

        sign = ""
        if total_outcome > 0:
            sign = "+"

        self.__log_string("Total outcome: {}{}".format(sign, total_outcome))
        self.__output.append("")

    # prints a couple of managers' transfers in a during GW
    def print_table(self):
        self.__managers.sort(key=cmp_to_key(TransfersManager.cmp_gw_outcome))

        row_num = 1
        for manager in self.__managers:
            manager.format_outcome()

            manager.row_num = row_num
            row_num += 1

        list_of_lists = []
        wildcards = []  # and freehits as well; FH = single GW WC
        for manager in self.__managers:
            list_of_lists.append(manager.to_list())

            if manager.get_wc_info() is not None:
                wildcards.append(manager.get_wc_info())

        legend = ["[Legend:]",
                  "TM = Transfers Made, H = Hit(s),",
                  "Outcome: Points gained/lost from transfers,",
                  "TV = Team Value,", "Tot = TV + Bank\n"]

        for line in legend:
            self.__log_string(line)

        headers = ["No", "Manager",
                   "Transfers Out", "Transfers In",
                   "{} TM".format(self.__gw_name), "{} H".format(self.__gw_name),
                   "Outcome", "{} P".format(self.__gw_name),
                   "TV", "Bank", "Tot"]

        table_output = tabulate(list_of_lists,
                                headers=headers,
                                tablefmt="orgtbl", floatfmt=".1f",
                                numalign="center", stralign="center")

        self.__log_string(table_output)
        self.__log_string("")

        for wildcard in wildcards:
            self.__log_string(wildcard)
            self.__log_string("")

        formatter = "entry" if len(self.__managers) < 2 else "entries"
        print("{} {} have been loaded successfully.".format(len(self.__managers), formatter))

    def __init_managers(self):
        threads = []

        if self.__path != "":
            live_data_parser = LiveDataParser(self.__current_event)
            threads = list(map(lambda id_: TransfersManager(id_, self.__current_event, live_data_parser), self.__ids))

        else:
            gw_one = 1
            for i in range(gw_one, self.__current_event + 1):
                live_data_parser = LiveDataParser(i)
                manager = TransfersManager(self.__id_, i, live_data_parser)
                threads.append(manager)

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        return threads

    def __log_string(self, string):
        print(string)
        self.__output.append(string)
