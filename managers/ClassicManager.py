from managers.Manager import Manager

from parsers.EventDataParser import EventDataParser
from parsers.TeamDataParser import TeamDataParser


class Rival(Manager):
    def __init__(self, id_, current_event, is_dgw):
        super().__init__(id_, current_event)

        self.row_num = 0

        [self.__total_points, self.__overall_rank, self.__gw_points] = [0, 0, 0]

        self.gw_points_string = ""
        self.used_chips_string = ""

        [self.gw_transfers, self.gw_hits] = [0, 0]
        [self.squad_value, self.money_itb, self.team_value] = [0.0, 0.0, 0.0]

        self.players_played = self.dgw_players_played = ""

        self.is_dgw = is_dgw

    def run(self):
        self.__init_all_properties()

    # This method is used a list of managers to get sorted by 'overall_rank' field
    def overall_rank(self):
        return self.__overall_rank

    def get_team_value(self):
        return self.team_value

    # This method is used a list of managers to get sorted by 'gw_points' attribute
    def gw_points(self):
        # TO-DO (!!!): If two or more managers have the same GW score
        #              want to take into consideration their OR

        hit_cost = 4
        return self.__gw_points - self.gw_hits*hit_cost

    def to_list(self):
        result = [self.row_num, self.manager_name,
                  self.__overall_rank, self.__total_points, self.used_chips_string,
                  self.gw_points_string, self.captain_name, self.vice_captain_name, self.active_chip,
                  self.players_played,
                  self.gw_transfers, self.gw_hits,
                  self.squad_value, self.money_itb, self.team_value]

        if self.is_dgw:
            result.insert(10, self.dgw_players_played)

        return result

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
    # Example: 42(-4)
    # Explanation: gameweek score = 42 with 1 hit taken
    """
    def format_gw_points(self):
        self.gw_points_string = str(self.__gw_points)

        if self.gw_hits != 0:
            self.gw_points_string += "(-" + str(self.gw_hits*4) + ")"

    def format_players_played(self, count):
        self.players_played = self.players_played.format(count)

    def format_dgw_players_played(self, count, total_dgw_players):
        self.dgw_players_played = "{} / {}".format(count, total_dgw_players)

    def __init_all_properties(self):
        self.team_data_parser = TeamDataParser(self.id_)
        self.event_data_parser = EventDataParser(self.id_, self.current_event)

        self.manager_name = self.team_data_parser.get_manager_name()
        [self.__total_points, self.__overall_rank, self.__gw_points] = self.team_data_parser.get_ranks_and_points()

        # If any manager used none of his chips, the method will return "None"
        # Otherwise -- it returns a string of used chips, separated by commas.
        self.used_chips_by_gw = self.team_data_parser.get_used_chips_by_gw()
        self.used_chips_string = "None" if len(self.used_chips_by_gw) == 0 else ', '.join(self.used_chips_by_gw)

        captain_ids = self.event_data_parser.get_captains_id()
        [self.captain_id, self.vice_captain_id] = captain_ids

        self.captain_name = self.event_data_parser.get_player_name(self.captain_id)
        self.vice_captain_name = self.event_data_parser.get_player_name(self.vice_captain_id)

        self.active_chip = self.event_data_parser.get_active_chip()
        [self.gw_transfers, self.gw_hits] = self.team_data_parser.get_transfers()
        [self.squad_value, self.money_itb, self.team_value] = self.team_data_parser.get_funds()

        [self.players_played, self.players_ids] = self.event_data_parser.get_players_ids(self.active_chip)

        self.all_players_ids = self.event_data_parser.get_all_players_ids()

    def __repr__(self):
        print(self.manager_name)

        print(self.__total_points)
        print(self.__overall_rank)
        print(self.__gw_points)

        print(self.gw_transfers)
        print(self.gw_hits)

        print(self.squad_value)
        print(self.money_itb)
        print(self.team_value)

        print(self.players_played)
