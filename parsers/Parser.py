import requests
import time


class Parser:
    __url_prefix = "https://fantasy.premierleague.com/api/entry/{}/"

    _urls = {"team_data": __url_prefix,
             "event_data": __url_prefix + "event/{}/picks/",
             "team_data_history": __url_prefix + "history/"
             }

    DGW = {25, 32, 34, 35}  # TO-DO: DGWs are unknown at the moment

    def __init__(self, id_):
        self._id_ = id_

    def _get_url_data(self, url, curr_event=0):
        if url is None:
            raise ValueError("An invalid URL has been passed.")

        if url == "team_data":
            new_url = self._urls[url].format(self._id_)
        elif url == "event_data":
            new_url = self._urls[url].format(self._id_, curr_event)
        elif url == "team_data_history":
            new_url = self._urls[url].format(self._id_)
        else:
            raise ValueError("Invalid type of url has been passed.")

        too_many_requests = 429

        while True:
            response = requests.get(new_url)

            if response.status_code == too_many_requests:
                time.sleep(1)
            else:
                break

        return response.json()

    @staticmethod
    def _get_chip_name(chip):
        return {"3xc": "TC",
                "wildcard": "WC",
                "bboost": "BB",
                "freehit": "FH"}.get(chip, "None")
