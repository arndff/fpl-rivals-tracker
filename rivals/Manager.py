from parsers.TeamDataParser import TeamDataParser
from parsers.EventDataParser import EventDataParser

import threading


class Manager(threading.Thread):

    def __init__(self, id_, current_event):
        threading.Thread.__init__(self)

        self.id_ = id_
        self.current_event = current_event

        self.row_num = 0

        self.manager_name = ""
        [self.__total_points, self.__overall_rank, self.__gw_points] = [0, 0, 0]

        self.used_chips = self.used_chips_string = ""

        [self.captain_id, self.vice_captain_id] = [0, 0]
        self.captain_name = self.vice_captain_name = ""

        self.active_chip = ""
        [self.gw_transfers, self.gw_hits] = [0, 0]
        [self.team_value, self.money_itb] = [0.0, 0.0]

        self.players_ids = []
        self.players_played = ""

    def run(self):
        td = TeamDataParser(self.id_)
        ed = EventDataParser(self.id_, self.current_event)

        self.__init_all_properties(td, ed)

    # This method is used a list of managers to get sorted by 'overall_rank' field
    def overall_rank(self):
        return self.__overall_rank

    # This method is used a list of managers to get sorted by 'gw_points' attribute
    def gw_points(self):
        return self.__gw_points

    def to_list(self):
        return [self.row_num, self.manager_name,
                self.__overall_rank, self.__total_points, self.used_chips_string,
                self.__gw_points, self.captain_name, self.vice_captain_name, self.active_chip,
                self.players_played,
                self.gw_transfers, self.gw_hits,
                self.team_value, self.money_itb]

    """
    This method is used to format both overall_rank and total points columns before printing the SORTED array
    Will have effect once when any of the given players get higher than 999pts
    """
    def format_total_points_and_overall_rank(self):
        self.__overall_rank = "{:,}".format(self.__overall_rank)
        self.__total_points = "{:,}".format(self.__total_points)

    """
    # This method is used to format gameweek points column before printing the SORTED array
    # The point is to show a player's result concatenated with his hit(s) count (if any)
    # Example: 42(-4), explanation: gameweek score: 42 with 1 hit taken
    """
    def format_gw_points(self):
        self.gw_points = str(self.gw_points)

        if self.gw_hits != 0:
            self.gw_points = "(-" + str(self.gw_hits) + ")"

    def format_players_played(self, count):
        self.players_played = self.players_played.format(count)

    def __init_all_properties(self, td, ed):
        self.manager_name = td.get_manager_name()
        [self.__total_points, self.__overall_rank, self.__gw_points] = td.get_ranks_and_points_info()

        # If any manager used none of his chips, the method will return "None"
        # Otherwise -- it returns a string of used chips, separated by commas.
        self.used_chips = td.get_used_chips_info()
        self.used_chips_string = "None" if len(self.used_chips) == 0 else ', '.join(self.used_chips)

        captain_ids = ed.get_captains_id()
        [self.captain_id, self.vice_captain_id] = captain_ids

        self.captain_name = ed.get_player_name(self.captain_id)
        self.vice_captain_name = ed.get_player_name(self.vice_captain_id)

        self.active_chip = ed.get_active_chip()
        [self.gw_transfers, self.gw_hits] = td.get_transfers_info()
        [self.team_value, self.money_itb] = td.get_funds_info()

        players = ed.get_players_ids(self.active_chip)
        self.players_played = players[0]
        self.players_ids = players[1]

    def __repr__(self):
        return self.manager_name
