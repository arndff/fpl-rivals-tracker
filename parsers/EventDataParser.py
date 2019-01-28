from parsers.Parser import Parser


class EventDataParser(Parser):
    def __init__(self, id_, curr_event):
        super().__init__(id_)
        self.__curr_event = curr_event
        self.__data = super()._get_url_data("event_data", self.__curr_event)

    # returns a tuple of captain's id and vice captain's id
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
    @staticmethod
    def get_player_name(captain_id, fpl_db):
        captain_name = None

        for entry in fpl_db["elements"]:
            if entry['id'] == captain_id:
                captain_name = entry["web_name"]
                break

        return captain_name

    def get_active_chip(self):
        return super()._get_chip_name(self.__data["active_chip"])

    def get_hits_count(self):
        return self.__data["entry_history"]["event_transfers_cost"]

    """
    return a set of players ids from starting xi 
    N.B.: if a specific player got subbed off, 
          the function replaces his id with the player's one who came in
    """
    def get_players_ids(self):
        auto_subs = self.get_autosubs()
        players_ids = set()
        players_added = 0

        for entry in self.__data["picks"]:
            current_id = entry["element"]

            if current_id in auto_subs:
                players_ids.add(auto_subs[current_id])
            else:
                players_ids.add(current_id)

            players_added += 1

            # if 11 players have already been added, the for loop ends
            if players_added == 11:
                break

        return players_ids

    """
    returns a dictionary which keys are the ids of subbed off players
    and values -- subbed in ones (talking about ids again)
    """
    def get_autosubs(self):
        auto_subs = {}

        for entry in self.__data["automatic_subs"]:
            auto_subs[entry["element_out"]] = entry["element_in"]

        return auto_subs
