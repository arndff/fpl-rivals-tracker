from parsers.Parser import Parser


class TeamDataParser(Parser):
    __FPL_CUP_CODE = 314  # Don't know if FPL Cup's code will be the same as season 18/19

    def __init__(self, id_):
        super().__init__(id_)
        self.__data = super()._get_url_data("team_data")
        self.__data_history = super()._get_url_data("team_data_history")

    """
    returns a string with manager's name
    team name could be added but it isn't necessary atm
    """
    def get_manager_name(self):
        values = ["player_first_name", "player_last_name"]

        return ' '.join(self.__data[value] for value in values)

    """
    returns a list where:
    numbers[0] = total points so far
    numbers[1] = player's overall rank (OR)
    numbers[2] = current GW points
                 (or the last one which has already taken place)
    """
    def get_ranks_and_points(self):
        values = ["summary_overall_points", "summary_overall_rank", "summary_event_points"]

        return [self.__data[value] for value in values]

    def get_used_chips_by_gw(self):
        used_chips = []
        wc_count = 0  # variable to help setting the two wildcard chips names' properly
        chips_history = self.__data_history["chips"]

        for chip in chips_history:
            chip_name = super()._get_chip_name(chip["name"])
            chip_used_at = chip["event"]

            result = self.__check_if_curr_chip_is_wc(chip_name, wc_count)
            wc_count = result[1]

            chip_string = "{}:{}".format(result[0], chip_used_at)
            used_chips.append(chip_string)

        return used_chips

    # TO-DO: test
    """
    returns a list where:
    transfers[0] = transfers made for the upcoming event
    transfers[1] = indicates how many hits have been taken (if any)
    """
    def get_transfers(self):
        values = ["event_transfers", "event_transfers_cost"]
        transfers = [self.__data_history["current"][0][value] for value in values]

        one_hit_cost = 4

        transfers[1] //= one_hit_cost  # hits count

        return transfers

    """
    returns a list where:
    funds[0] = team value
    funds[1] = money in the bank (ITB)
    the sum of these two will give you 'team value (TV)' which is higher than 'sell value (SV)'
    """
    def get_funds(self):
        values = ["value", "bank"]
        funds = [self.__data_history["current"][self.get_current_event() - 1][value] for value in values]

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

        return funds

    # TO-DO: Test the method once when FPL Cup starts
    """
    def get_cup_opponent(self):
        cup_data = self.__data["leagues"]["cup"]

        if len(cup_data) == 0:
            return -1

        cup_data_event = cup_data[0][0]["event"]

        if cup_data_event != self.get_current_event():
            return -1
        elif cup_data_event == self.get_current_event():
            entry_1 = cup_data[0][0]["entry_1_entry"]
            entry_2 = cup_data[0][0]["entry_2_entry"]

            if entry_1 == self._id_:
                return entry_2
            elif entry_2 == self._id_:
                return entry_1
    """

    def get_cup_opponent(self):
        return -1

    """
    this method returns a dictionary:
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

        # Ignoring FPL Cup
        if self.__FPL_CUP_CODE in league_codes:
            del league_codes[self.__FPL_CUP_CODE]

        return league_codes

    """
    get the number of the current event
    it'll be used in EventDataParser class to make a request to a specific url which requires it
    """
    def get_current_event(self):
        return self.__data["current_event"]

    @staticmethod
    def __check_if_curr_chip_is_wc(chip_name, count):
        if chip_name == "WC":
            if count == 0:
                chip_name += "1"
            elif count == 1:
                chip_name += "2"

            count += 1

        result = (chip_name, count)

        return result
