from managers.Manager import Manager

from parsers.EventDataParser import EventDataParser
from parsers.TeamDataParser import TeamDataParser


class Opponent(Manager):
    def __init__(self, id_, current_event, set_leagues, league_name=""):
        super().__init__(id_, current_event)

        self.__set_leagues = set_leagues
        self.leagues = {}

        self.league_name = league_name

    def run(self):
        self.__init_all_properties()

    def __init_all_properties(self):
        self.team_data_parser = TeamDataParser(self.id_)
        self.event_data_parser = EventDataParser(self.id_, self.current_event)

        self.manager_name = self.team_data_parser.get_manager_name()

        [self.captain_id, self.vice_captain_id] = self.event_data_parser.get_captains_id()
        self.captain_name = self.event_data_parser.get_player_name(self.captain_id)
        self.vice_captain_name = self.event_data_parser.get_player_name(self.vice_captain_id)

        self.gw_hits = self.team_data_parser.get_transfers()[1]

        if self.__set_leagues:
            self.leagues = self.team_data_parser.get_h2h_league_codes()

        self.active_chip = self.event_data_parser.get_active_chip()

        self.players_ids = self.event_data_parser.get_players_ids(self.active_chip)[1]
