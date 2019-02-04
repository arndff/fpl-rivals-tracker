import requests

from parsers.Parser import Parser


class HthParser(Parser):
    __url = "https://fantasy.premierleague.com/drf/leagues-h2h-standings/{}"

    def __init__(self, id_, leagues):
        super().__init__(id_)
        self.__leagues = leagues

    def get_opponent_id(self, league_code):
        response = requests.get(self.__url.format(league_code))
        data = super()._extract_values(response.json(), "matches_this", ["results"])

        for element in data[0]:
            match = (element["entry_1_entry"], element["entry_2_entry"])

            if match[0] == self._id_:
                return match[1]
            elif match[1] == self._id_:
                return match[0]

    """
    self.__leagues is a dictionary:
    - keys are leagues codes
    - values are strings = names of these leagues
    result is a dictionary:
    - keys are opponent ids
    - values are strings = names of the league where the match is going to be played
    """
    def get_opponents_ids(self):
        result = {}

        for key, value in self.__leagues.items():
            opponent_id = self.get_opponent_id(key)

            if opponent_id is not None:
                result[opponent_id] = value

        return result
