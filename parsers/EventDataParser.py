import sys
import requests

from parsers.Parser import Parser


class EventDataParser(Parser):
    try:
        # This data is fine to be requested just once as it doesn't depend on a particular id
        __FPL_DB = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
    except ValueError:
        print("Probably the game is being updated...")
        print("Try again 15 minutes before the early kick-off.")
        sys.exit(1)

    def __init__(self, id_, current_event):
        super().__init__(id_)
        # self.__current_event = current_event
        self.__data = super()._get_url_data("event_data", current_event)

    # Returns a tuple of captain's id and vice captain's id
    def get_captains_id(self):
        picks = self.__data["picks"]
        captain_id = -1
        vice_captain_id = -1

        for entry in picks:
            if entry["is_captain"]:
                captain_id = entry["element"]
            elif entry["is_vice_captain"]:
                vice_captain_id = entry["element"]

            if captain_id != -1 and vice_captain_id != -1:
                break

        captains = (captain_id, vice_captain_id)

        return captains

    # The method is used to extract captain's / vice captain's name
    def get_player_name(self, player_id):
        return self.__find_player_property(player_id, "web_name")

    def get_player_team(self, player_id):
        team_id = self.__find_player_property(player_id, "team")

        for team in self.__FPL_DB["teams"]:
            if team["id"] == team_id:
                return team["short_name"]

    def get_active_chip(self):
        return super()._get_chip_name(self.__data["active_chip"])

    def get_all_players_ids(self):
        players_ids = []

        for entry in self.__data["picks"]:
            current_id = entry["element"]
            players_ids.append(current_id)

        return players_ids

    def get_players_ids(self, active_chip):
        if active_chip == "BB":
            players_played = "{} / 15"
            players_ids = self.__get_players_ids_with_bb()
        else:
            players_played = "{} / 11"
            players_ids = self.__get_players_ids()

        result = (players_played, players_ids)

        return result

    def __find_player_property(self, player_id, property_):
        for entry in self.__FPL_DB["elements"]:
            if entry["id"] == player_id:
                return entry[property_]

    """
    Return a set of players IDs from starting XI
    - if a specific player got subbed off, 
      the function replaces his id with the player's one who came in
    """
    def __get_players_ids(self):
        auto_subs = self.__get_autosubs()
        players_ids = set()
        players_added = 0
        total_players = 11

        for entry in self.__data["picks"]:
            current_id = entry["element"]

            if current_id in auto_subs:
                players_ids.add(auto_subs[current_id])
            else:
                players_ids.add(current_id)

            players_added += 1

            # if 11 players have already been added, the for loop ends
            if players_added == total_players:
                break

        return players_ids

    """
    Returns a dictionary:
    - keys are the ids of subbed off players
    - values -- subbed in ones' (talking about IDs again)
    """
    def __get_autosubs(self):
        auto_subs = {}

        for entry in self.__data["automatic_subs"]:
            auto_subs[entry["element_out"]] = entry["element_in"]

        return auto_subs

    """
    Returns all 15 players' ids because BB chip has been activated
    """
    def __get_players_ids_with_bb(self):
        players_ids = set()

        for entry in self.__data["picks"]:
            current_id = entry["element"]
            players_ids.add(current_id)

        return players_ids
