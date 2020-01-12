from managers.Manager import Manager
from parsers.EventDataParser import EventDataParser
from parsers.TeamDataParser import TeamDataParser
from parsers.TransfersParser import TransfersParser


class BasicManager(Manager):
    def __init__(self, id_, current_event, live_data_parser=None):
        super().__init__(id_, current_event)
        self.__live_data_parser = live_data_parser

        self.row_num = 0

    def run(self):
        self.__init_all_properties()

    # This method is used a list of managers to get sorted by 'outcome' field
    def outcome(self):
        return self.__outcome

    def format_outcome(self):
        sign = ""

        if self.__outcome > 0:
            sign = "+"

        self.__outcome = "{}{}".format(sign, self.__outcome)

    def to_list(self):
        result = [self.row_num, self.manager_name,
                  self.sold_players, self.bought_players,
                  self.gw_transfers, self.gw_hits,
                  self.__outcome, self.gw_points_string,
                  self.squad_value, self.money_itb, self.team_value]

        return result

    def to_list_gw(self):
        result = [self.current_event,
                  self.sold_players, self.bought_players,
                  self.gw_transfers, self.gw_hits,
                  self.__outcome]

        return result

    def __init_all_properties(self):
        self.team_data_parser = TeamDataParser(self.id_)
        self.event_data_parser = EventDataParser(self.id_, self.current_event)
        self.transfers_data_parser = TransfersParser(self.id_, self.current_event,
                                                     self.event_data_parser, self.__live_data_parser)

        self.manager_name = self.team_data_parser.get_manager_name()
        self.overall_rank = "{:,}".format(self.team_data_parser.get_ranks_and_points()[1])
        self.active_chip = self.event_data_parser.get_active_chip()

        if self.active_chip != "WC":
            (self.sold_players, self.bought_players,
             self.sold_players_points, self.bought_players_points) = self.transfers_data_parser.get_transfers()
        else:
            (self.sold_players, self.bought_players,
             self.sold_players_points, self.bought_players_points) = ("WC ACTIVE", "WC ACTIVE", 0, 0)

        (self.gw_transfers, self.gw_hits) = self.team_data_parser.get_transfers_gw(self.current_event)
        self.__outcome = self.bought_players_points - self.sold_players_points - self.gw_hits*4

        self.gw_points_string = str(self.team_data_parser.get_ranks_and_points()[2])

        if self.gw_hits != 0:
            self.gw_points_string += "(-" + str(self.gw_hits * 4) + ")"

        (self.squad_value, self.money_itb, self.team_value) = self.team_data_parser.get_funds()

