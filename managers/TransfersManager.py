from managers.Manager import Manager
from parsers.EventDataParser import EventDataParser
from parsers.TeamDataParser import TeamDataParser
from parsers.TransfersParser import TransfersParser


class TransfersManager(Manager):
    def __init__(self, id_, current_event, live_data_parser=None):
        super().__init__(id_, current_event)
        self.__live_data_parser = live_data_parser

        self.__sold_players = self.__bought_players = ""
        self.outcome = None

        self.row_num = 0

    def run(self):
        self.__init_all_properties()

    def format_outcome(self):
        sign = ""
        if self.outcome > 0:
            sign = "+"

        self.outcome = "{}{}".format(sign, self.outcome)

    def to_list(self):
        if self.event_data_parser.get_active_chip() == "WC":
            self.__sold_players = self.__bought_players = "WC ACTIVE"

        result = [self.row_num, self.__manager_name,
                  self.__sold_players, self.__bought_players,
                  self.gw_transfers, self.gw_hits,
                  self.outcome, self.__gw_points_string,
                  self.__squad_value, self.__money_itb, self.__team_value]

        return result

    def to_list_gw(self):
        if self.__active_chip == "WC" or self.__active_chip == "FH":
            self.__sold_players = self.__bought_players = "{} ACTIVE".format(self.__active_chip)

        rank_in_specific_gw = self.team_data_parser.get_overall_rank_in_specific_gw(self._current_event)

        result = [self._current_event, rank_in_specific_gw,
                  self.__sold_players, self.__bought_players,
                  self.gw_transfers, self.gw_hits,
                  self.outcome]

        return result

    def get_wc_info(self):
        return self.__wc_info

    @staticmethod
    def cmp_gw_outcome(left, right):
        if left.outcome < right.outcome:
            return 1
        elif left.outcome > right.outcome:
            return -1
        else:
            if left.gw_transfers > right.gw_transfers:
                return 1
            elif left.gw_transfers == right.gw_transfers:
                return 0
            else:
                return -1

    def __init_all_properties(self):
        self.__init_parsers()

        self.__gw_name = self.team_data_parser.get_gw_name(self._current_event)

        self.__manager_name = self.team_data_parser.get_manager_name()
        self.overall_rank = "{:,}".format(self.team_data_parser.get_ranks_and_points()[1])
        self.__active_chip = self.event_data_parser.get_active_chip()

        self.__init_sold_and_bought_players()

        (self.gw_transfers, self.gw_hits) = self.team_data_parser.get_transfers_gw(self._current_event)
        self.outcome = self.__bought_players_points - self.__sold_players_points - self.gw_hits*4

        self.__gw_points_string = str(self.team_data_parser.get_ranks_and_points()[2])

        if self.gw_hits != 0:
            self.__gw_points_string += "(-" + str(self.gw_hits * 4) + ")"

        (self.__squad_value, self.__money_itb, self.__team_value) = self.team_data_parser.get_funds()

        self.__wc_info = self.__init_wc_info()

    def __init_parsers(self):
        self.team_data_parser = TeamDataParser(self._id)
        self.event_data_parser = EventDataParser(self._id, self._current_event)
        self.transfers_data_parser = TransfersParser(self._id, self._current_event,
                                                     self.event_data_parser, self.__live_data_parser)

    def __init_sold_and_bought_players(self):
        transfers_ids = self.__init_transfers_ids()
        self.transfers_data_parser.set_transfers_ids(transfers_ids)

        (self.__sold_players, self.__bought_players,
         self.__sold_players_points, self.__bought_players_points) = self.transfers_data_parser.get_transfers()

    def __init_wc_transfers_ids(self):
        players_ids_previous_gw = EventDataParser(self._id, self._current_event - 1).get_players_ids("BB")[1]
        players_ids_current_gw = self.event_data_parser.get_players_ids("BB")[1]

        unique_players_prev_gw = players_ids_previous_gw - players_ids_current_gw
        self.__unique_players_curr_gw = players_ids_current_gw - players_ids_previous_gw

        transfers_ids = []
        for i in range(0, len(unique_players_prev_gw)):
            pair = (unique_players_prev_gw[i], self.__unique_players_curr_gw[i])
            transfers_ids.append(pair)

        return transfers_ids

    """
    transfers_ids are going to be set
    IF the active chip is WC or FH
    ELSE -> None
    """
    def __init_transfers_ids(self):
        transfers_ids = None

        if self.__active_chip == "WC" or self.__active_chip == "FH":
            if self.__active_chip == "WC":
                self.gw_hits = "WC1" if self._current_event < 21 else "WC2"
            elif self.__active_chip == "FH":
                self.gw_hits = "FH"

            transfers_ids = self.__init_wc_transfers_ids()

        return transfers_ids

    """
    That method handles the FH chip as well,
    which is actually a single GW wildcard
    """
    def __init_wc_info(self):
        if self.__active_chip == "WC" or self.__active_chip == "FH":
            self.gw_transfers = len(self.__sold_players.split(","))

            sign = ""
            if self.outcome > 0:
                sign = "+"

            return "[{} {}:]\n{}\nTransfers Out: {}\nTransfers In: {}\nOutcome: {}{}"\
                   .format(self.__manager_name, self.__active_chip, self.__gw_name,
                           self.__sold_players, self.__bought_players,
                           sign, self.outcome)
        else:
            return None

    def __repr__(self):
        result = "{}, {}, {}, {}, {}".format(self.row_num,
                                             self.__manager_name,
                                             self.gw_transfers,
                                             self.gw_hits,
                                             self.outcome)

        return result
