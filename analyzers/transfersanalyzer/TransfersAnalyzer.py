from abc import ABC, abstractmethod

from analyzers.utility_functions import get_gw_info


class TransfersAnalyzer(ABC):
    _WC_MSG = "[WC outcome:] (Transfers IN - Transfers OUT) [incl. bench points]\n"

    [_current_event, _gw_name, _] = get_gw_info()

    @abstractmethod
    def save_output_to_file(self):
        pass

    @abstractmethod
    def print_table(self):
        pass

    @abstractmethod
    def _init_managers(self):
        pass

    @abstractmethod
    def _print_table_output(self):
        pass

    @abstractmethod
    def _print_wc_fh_info(self):
        pass

