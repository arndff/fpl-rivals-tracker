from parsers.Parser import Parser


class TeamDataParser(Parser):
    def __init__(self, id_):
        super().__init__(id_)
        self.__data = super()._get_url_data("team_data")

    """
    returns a string with manager's name
    team name could be added but it isn't necessary atm
    """
    def get_manager_name(self):
        values = ["player_first_name", "player_last_name"]
        names = self.__extract_values("entry", values)
        return ' '.join([names[0], names[1]])

    """
    returns a list where:
    numbers[0] = total points so far
    numbers[1] = player's overall rank (OR)
    numbers[2] = current GW points
                 (or the last one which has already taken place)
    """
    def get_ranks_and_points_info(self):
        values = ["summary_overall_points", "summary_overall_rank", "summary_event_points"]
        numbers = self.__extract_values("entry", values)

        return numbers

    def get_used_chips_info(self):
        chips_history = self.__data["chips"]
        used_chips = set()
        count = 0  # variable to help setting the two wildcard chips names' properly

        for chip in chips_history:
            chip_name = super()._get_chip_name(chip["name"])

            if chip_name == "WC":
                if count == 0:
                    chip_name += "1"
                elif count == 1:
                    chip_name += "2"

                count += 1

            used_chips.add(chip_name)

        return used_chips

    """
    returns a list where:
    transfers[0] = transfers made for the upcoming event
    transfers[1] = indicates how many hits have been taken (if any)
    """
    def get_transfers_info(self):
        values = ["event_transfers", "event_transfers_cost"]
        transfers = self.__extract_values("entry", values)

        transfers[1] //= 4  # hits count

        return transfers

    """
    returns a list where:
    funds[0] = team value
    funds[1] = money in the bank (ITB)
    the sum of these two will give you 'team value (TV)' which is higher than 'sell value (SV)'
    """
    def get_funds_info(self):
        values = ["value", "bank"]
        funds = self.__extract_values("entry", values)

        funds[0] /= 10  # team value

        """
        If money ITB:
        (1) 5 ~> 0.5
        (2) 13 ~> 1.3
        """

        if funds[1] < 10:
            funds[1] *= 0.1
        else:
            funds[1] /= 10

        return funds

    """
    this method returns a dictionary:
    - keys are an integer which is a h2h code
    - values are strings, associated with given h2h league code
    """
    def get_h2h_league_codes(self):
        h2h_leagues = self.__extract_values("leagues", ["h2h"])
        league_codes = {}

        for league in h2h_leagues[0]:
            league_name = league["name"]
            league_code = league["id"]
            league_codes[league_code] = league_name

        FPL_CUP_CODE = 314

        # Ignoring FPL Cup for now
        if FPL_CUP_CODE in league_codes:
            """
            tmp = league_codes[-1]
            league_codes[-1] = league_codes[0]
            league_codes[0] = tmp

            league_codes.pop()
            """

            del league_codes[FPL_CUP_CODE]

        return league_codes

    """
    get the number of the current event
    it'll be used in EventDataParser class to make a request to a specific url which requires it
    """
    def get_current_event(self):
        return self.__data["entry"]["current_event"]

    def __extract_values(self, key, values):
        return super()._extract_values(self.__data, key, values)
