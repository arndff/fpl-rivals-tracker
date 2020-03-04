import requests
import time


class Parser:
    __url_prefix = "https://fantasy.premierleague.com/api/entry/{}/"

    _urls = {"team_data": __url_prefix,
             "team_data_history": __url_prefix + "history/",
             "event_data": __url_prefix + "event/{}/picks/",
             "transfers": __url_prefix + "transfers/"
             }

    BGW = {18, 28, 31, 34}
    DGW = {24, 29, 37}

    def __init__(self, id_):
        self._id = id_

    def _get_url_data(self, url, curr_event=0):
        if url is None:
            raise ValueError("URL cannot be None.")

        if url == "team_data":
            new_url = self._urls[url].format(self._id)
        elif url == "team_data_history":
            new_url = self._urls[url].format(self._id)
        elif url == "event_data":
            new_url = self._urls[url].format(self._id, curr_event)
        elif url == "transfers":
            new_url = self._urls[url].format(self._id)
        else:
            raise ValueError("Invalid type of url has been passed.")

        response = self._read_response(new_url)
        return response.json()

    @staticmethod
    def _get_chip_name(chip):
        return {"3xc": "TC",
                "wildcard": "WC",
                "bboost": "BB",
                "freehit": "FH"}.get(chip, "None")

    @staticmethod
    def _read_response(new_url):
        too_many_requests = 429

        while True:
            response = requests.get(new_url)

            if response.status_code == too_many_requests:
                time.sleep(1)
            else:
                break

        return response
