import requests


class LiveDataParser:
    __live_data_url = "https://fantasy.premierleague.com/drf/event/{}/live"

    def __init__(self, curr_event, is_dgw=False):
        self.__live_data = requests.get(self.__live_data_url.format(curr_event)).json()
        self.__all_players = self.__live_data["elements"]
        self.__is_dgw = is_dgw

    def count_players_played(self, players_ids):
        if not self.__is_dgw:
            return self.__players_played_in_sgw(players_ids)
        else:
            return self.__players_played_in_dgw(players_ids)

    def get_player_points(self, player_id):
        return self.__all_players[str(player_id)]["stats"]["total_points"]

    """
    returns dgw players count
    """
    def get_dgw_players_count(self, players_ids):
        count = 0

        for player_id in players_ids:
            player_data = self.__all_players[str(player_id)]["explain"]

            if len(player_data) == 2:
                count += 1

        return count

    def __players_played_in_sgw(self, players_ids):
        count = 0

        for player_id in players_ids:
            minutes_played = self.__all_players[str(player_id)]["explain"][0][0]["minutes"]["value"]

            if minutes_played > 0:
                count += 1

        return count

    def __players_played_in_dgw(self, players_ids):
        count = 0

        for player_id in players_ids:
            player_data = self.__all_players[str(player_id)]["explain"]

            if len(player_data) == 1:
                minutes_played = player_data[0][0]["minutes"]["value"]

                if minutes_played > 0:
                    count += 1
            else:
                for game in player_data:
                    minutes_played = game[0]["minutes"]["value"]

                    if minutes_played > 0:
                        count += 1
                        break

        return count
