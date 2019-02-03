from parsers.TeamDataParser import TeamDataParser
from parsers.EventDataParser import EventDataParser

import threading


class Manager(threading.Thread):
    def __init__(self, id_, current_event, set_leagues, league_name=""):
        threading.Thread.__init__(self)

        self.id_ = id_
        self.current_event = current_event

        self.td = TeamDataParser(self.id_)
        self.ed = EventDataParser(self.id_, self.current_event)

        self.manager_name = ""

        self.captain_id = 0
        self.captain_name = ""

        self.players_ids = []

        self.__set_leagues = set_leagues
        self.leagues = {}

        self.league_name = league_name

        self.active_chip = ""

    def run(self):
        self.__init_all_properties(self.td, self.ed)

    def __init_all_properties(self, td, ed):
        self.manager_name = td.get_manager_name()

        captain_ids = ed.get_captains_id()
        self.captain_id = captain_ids[0]
        self.captain_name = ed.get_player_name(self.captain_id)

        if self.__set_leagues:
            self.leagues = td.get_h2h_league_codes()

        self.active_chip = self.ed.get_active_chip()

        self.players_ids = self.ed.get_players_ids(self.active_chip)[1]
