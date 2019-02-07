import requests
import time


class Parser:
    __url_prefix = "https://fantasy.premierleague.com/drf/entry/{}"

    _urls = {"team_data": __url_prefix + "/history",
             "event_data": __url_prefix + "/event/{}/picks",
             }

    DGW = [25, 32, 35]

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
            new_url = self._urls[url].format(self._id_)
        elif url == "event_data":
            new_url = self._urls[url].format(self._id_, curr_event)
        else:
            raise ValueError("Invalid type of url has been passed.")

        while True:
            response = requests.get(new_url)
            if response.status_code == 429:
                time.sleep(1)
            else:
                break

        return response.json()

    @staticmethod
    def _extract_values(data, key, values):
        return [data[key][value] for value in values]

    @staticmethod
    def _get_chip_name(chip):
        return {"3xc": "TC",
                "wildcard": "WC",
                "bboost": "BB",
                "freehit": "FH"}.get(chip, "None")
