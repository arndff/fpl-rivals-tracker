import sys

from parsers.Parser import Parser


class TeamDataParser(Parser):
    # __FPL_CUP_CODE = 314  # Don't know if FPL Cup's code will be the same as season 18/19

    __UPDATE_MSG = "The game is being updated."

    def __init__(self, id_):
        super().__init__(id_)
        self.__data = super()._get_url_data("team_data")

        if self.__data == self.__UPDATE_MSG:
            print("The game is being updated.")
            print("Please try again later when the updated scores / teams will be available.")
            sys.exit(1)

        self.__data_history = super()._get_url_data("team_data_history")

    def get_manager_name(self):
        values = ["player_first_name", "player_last_name"]
        return ' '.join(self.__data[value] for value in values)

    """
    Returns a list where:
    numbers[0] = total points so far
    numbers[1] = player's overall rank (OR)
    numbers[2] = current GW points
                 (or the last one which has already taken place)
    """
    def get_ranks_and_points(self):
        values = ["summary_overall_points", "summary_overall_rank", "summary_event_points"]

        return [self.__data[value] for value in values]

    def get_overall_rank_in_specific_gw(self, gw):
        return "{:,}".format(self.__data_history["current"][gw - 1]["overall_rank"])

    def get_used_chips_by_gw(self):
        used_chips = []
        wc_count = 0  # Variable to help setting the two wildcard chips names' properly
        chips_history = self.__data_history["chips"]

        for chip in chips_history:
            chip_name = super()._get_chip_name(chip["name"])
            chip_used_at = chip["event"]

            result = self.__is_chip_wc(chip_name, wc_count)
            wc_count = result[1]

            chip_string = "{}:{}".format(result[0], chip_used_at)
            used_chips.append(chip_string)

        return used_chips

    """
    Returns a list where:
    transfers[0] = transfers made for the upcoming event
    transfers[1] = indicates how many hits have been taken (if any)
    """
    def get_transfers(self):
        values = ["event_transfers", "event_transfers_cost"]
        length = len(self.__data_history["current"])
        transfers = [self.__data_history["current"][length - 1][value] for value in values]

        hit_cost = 4
        transfers[1] //= hit_cost  # Hits count

        return transfers

    def get_transfers_gw(self, gw):
        values = ["event_transfers", "event_transfers_cost"]
        transfers = [self.__data_history["current"][gw - 1][value] for value in values]

        hit_cost = 4
        transfers[1] //= hit_cost  # Hits count

        return transfers

    """
    Returns a list where:
    funds[0] = squad value
    funds[1] = money in the bank (ITB)
    funds[2] = funds[0] + funds[1]
    the sum of these two will give you 'team value (TV)' which is higher than 'sell value (SV)'
    """
    def get_funds(self):
        values = ["value", "bank"]
        length = len(self.__data_history["current"])
        funds = [self.__data_history["current"][length - 1][value] for value in values]

        base = 10
        multiplier = 0.1

        funds[0] /= base  # team value

        """
        If money ITB:
        (1) 5 ~> 0.5
        (2) 13 ~> 1.3
        """
        if funds[1] < base:
            funds[1] *= multiplier
        else:
            funds[1] /= base

        funds[0] -= funds[1]

        team_value = funds[0] + funds[1]
        funds.append(team_value)

        return funds

    def get_cup_opponent(self):
        cup_data = self.__data["leagues"]["cup"]["matches"]

        # cup_data["status"]["qualification_state"] == "NOT_QUALIFIED_RANK" || ?

        if len(cup_data) == 0:
            return -1

        if cup_data[0]["event"] != self.get_current_event():
            return -1
        else:
            entry_1 = cup_data[0]["entry_1_entry"]
            entry_2 = cup_data[0]["entry_2_entry"]

            if entry_1 == self._id_:
                return entry_2
            elif entry_2 == self._id_:
                return entry_1

    """
    Returns a dictionary:
    - keys are an integer which is a h2h code
    - values are league names, associated with given h2h league code
    """
    def get_h2h_league_codes(self):
        h2h_leagues = self.__data["leagues"]["h2h"]
        league_codes = {}

        for league in h2h_leagues:
            league_name = league["name"]
            league_code = league["id"]
            league_codes[league_code] = league_name

        """
        # Ignoring FPL Cup
        if self.__FPL_CUP_CODE in league_codes:
            del league_codes[self.__FPL_CUP_CODE]
        """

        return league_codes

    def get_bench_points_in_specific_gw(self, gw):
        return self.__data_history["current"][gw - 1]["points_on_bench"]

    """
    get the number of the current event
    it'll be used in EventDataParser class to make a request to a specific url which requires it
    """
    def get_current_event(self):
        return self.__data["current_event"]

    def get_gw_name(self, current_event):
        if current_event in self.BGW:
            prefix = "BGW"
        elif current_event in self.DGW:
            prefix = "DGW"
        else:
            prefix = "GW"

        return "{}{}".format(prefix, current_event)

    @staticmethod
    def __is_chip_wc(chip_name, count):
        if chip_name == "WC":
            if count == 0:
                chip_name += "1"
            elif count == 1:
                chip_name += "2"

            count += 1

        result = (chip_name, count)
        return result
