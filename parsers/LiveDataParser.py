import requests


class LiveDataParser:
    __live_data_url = "https://fantasy.premierleague.com/drf/event/{}/live"

    def __init__(self, curr_event):
        self.__live_data = requests.get(self.__live_data_url.format(curr_event)).json()
        self.__all_players = self.__live_data["elements"]

    def count_players_played(self, players_ids):
        count = 0

        for entry in self.__all_players:
            minutes_played = self.__all_players[entry]["explain"][0][0]["minutes"]["value"]

            # players_ids contains integers
            # while 'entry' is a string, so that's the reason why it must be casted to int
            if int(entry) in players_ids:
                if minutes_played > 0:
                    count += 1

        return count





