import requests

from parsers.TeamDataParser import TeamDataParser
from parsers.Parser import Parser


class HthParser(Parser):
    __url = "https://fantasy.premierleague.com/api/leagues-h2h-matches/league/{}/?page={}&event={}"

    def __init__(self, id_, leagues):
        super().__init__(id_)
        self.__leagues = leagues
        self.__current_event = TeamDataParser(1).get_current_event()

    def get_opponent_id(self, session, league_code, page_cnt):
        new_url = self.__url.format(league_code, page_cnt, self.__current_event)
        response = session.get(new_url).json()
        # has_next = response["has_next"]

        data = response["results"]
        result = -1

        for element in data:
            match = (element["entry_1_entry"], element["entry_2_entry"])

            if match[0] == self._id_:
                result = match[1]
            elif match[1] == self._id_:
                result = match[0]

        if result != -1:
            return result
        else:
            return self.get_opponent_id(session, league_code, page_cnt + 1)

    # TO-DO: dummy acc
    def auth(self, user, password):
        session = requests.session()
        login_url = 'https://users.premierleague.com/accounts/login/'
        payload = {
            'password': password,
            'login': user,
            'redirect_uri': 'https://fantasy.premierleague.com/a/login',
            'app': 'plfpl-web'
        }

        session.post(login_url, data=payload)

        return session

    """
    self.__leagues is a dictionary:
    - keys are leagues codes
    - values are strings = names of these leagues
    result is a dictionary:
    - keys are opponent ids
    - values are strings = names of the league where the match is going to be played
    """
    def get_opponents_ids(self, user, password):
        result = {}
        session = self.auth(user, password)

        for key, value in self.__leagues.items():
            opponent_id = self.get_opponent_id(session, key, 1)

            if opponent_id is not None:
                result[opponent_id] = value

        return result
