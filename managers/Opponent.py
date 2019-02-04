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
        self.tdp = TeamDataParser(self.id_)
        self.edp = EventDataParser(self.id_, self.current_event)

        self.manager_name = self.tdp.get_manager_name()

        captain_ids = self.edp.get_captains_id()
        self.captain_id = captain_ids[0]
        self.captain_name = self.edp.get_player_name(self.captain_id)
        self.vice_captain_id = captain_ids[1]
        self.vice_captain_name = self.edp.get_players_ids(self.vice_captain_id)

        if self.__set_leagues:
            self.leagues = self.tdp.get_h2h_league_codes()

        self.active_chip = self.edp.get_active_chip()

        self.players_ids = self.edp.get_players_ids(self.active_chip)[1]
