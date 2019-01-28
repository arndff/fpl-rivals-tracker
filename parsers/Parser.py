import requests
import sys
import time


class Parser:

    __URL_PREFIX = "https://fantasy.premierleague.com/drf/entry/{}"

    _URLS = {"team_data": __URL_PREFIX + "/history",
             "event_data": __URL_PREFIX + "/event/{}/picks",
             }

    def __init__(self, id_):
        self._id_ = id_

    """
    url *must* be one of these two:
    ["team_data", "event_data"]
    """
    def _get_url_data(self, url, curr_event=0):
        if url is None:
            raise ValueError("An invalid URL has been passed.")

        if url == "team_data":
            new_url = self._URLS[url].format(self._id_)
        elif url == "event_data":
            new_url = self._URLS[url].format(self._id_, curr_event)
        else:
            raise ValueError("Invalid type of url has been passed.")

        while True:
            response = requests.get(new_url)
            if response.status_code == 429:
                time.sleep(1)
            else:
                break

        try:
            return response.json()
        except requests.exceptions.RequestException:
            print("Probably the FPL API is down due to an update.")
            print("It happens right before each GW's deadline for less than an hour of time.")
            sys.exit(1)

    @staticmethod
    def _extract_values(data, key, values):
        return [data[key][value] for value in values]

    @staticmethod
    def _get_chip_name(chip):
        return {"3xc": "TC",
                "wildcard": "WC",
                "bboost": "BB",
                "freehit": "FH"}.get(chip, "None")
