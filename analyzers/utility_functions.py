import functools
import requests
import time

from fileutils.fileutils import extract_file_name_from_path
from parsers.TeamDataParser import TeamDataParser


MAIN_URL = "https://fantasy.premierleague.com/api/"
league_url = MAIN_URL + "leagues-classic/{}/standings/?page_new_entries={}&page_standings={}&phase={}"


def read_ids(ids_file, league_id=-1, managers_count=-1):
    if league_id == -1:
        ids = read_ids_from_file(ids_file)
    else:
        ids = extract_teams_ids_from_league_main(league_id, managers_count)

    return ids


def read_ids_from_file(path, my_id=-1):
    with open(path, "r") as input_file:
        lines = input_file.readlines()
        ids = {line.rstrip('\n') for line in lines}

        """
        - this is used in HthAnalyzer class when you want to compare your team to some others
        - the point is to remove your id (if it exists) from the given file with ids
          because it's pointless to compare your team to itself 
        """
        ids.discard(str(my_id))

    return ids


def extract_teams_ids_from_league_main(league_id, managers_count):
    session = auth()
    teams_ids = []
    page_standings = 1

    extract_ids_from_league(session, league_id, teams_ids, page_standings)
    if managers_count > 0:
        teams_ids = teams_ids[:managers_count]

    return teams_ids


def extract_ids_from_league(session, league_id, teams_ids, page_standings, page_new_entries=1, phase=1):
    formatted_url = league_url.format(league_id, 1, page_standings, 1)
    league_data = session.get(formatted_url).json()

    has_next = league_data["standings"]["has_next"]

    managers = league_data["standings"]["results"]
    for manager in managers:
        teams_ids.append(manager["entry"])

    if has_next:
        page_standings += 1
        extract_ids_from_league(session, league_id, teams_ids, page_standings)
    else:
        return teams_ids


def get_gw_info():
    manager_id = 1
    temp_team_data_parser = TeamDataParser(manager_id)

    current_event = temp_team_data_parser.get_current_event()
    gw_name = temp_team_data_parser.get_gw_name(current_event)
    is_dgw = current_event in temp_team_data_parser.DGW

    gw_info = [current_event, gw_name, is_dgw]
    return gw_info


def set_output_file(current_event, type_, ids_file, league_name, league_id):
    output_path = "output/{}.txt"

    if league_id == -1:
        file_name = "{}_{}_gw{}".format(extract_file_name_from_path(ids_file), type_, current_event)
    else:
        file_name = league_name

    return output_path.format(file_name)


def auth():
    session = requests.session()
    login_url = 'https://users.premierleague.com/accounts/login/'
    payload = {
        'password': "IvanIvanov90",
        'login': "deuces94@abv.bg",
        'redirect_uri': 'https://fantasy.premierleague.com/a/login',
        'app': 'plfpl-web'
    }

    session.post(login_url, data=payload)

    return session


def performance(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        f(self, *args, **kwargs)
        execution_time = time.time() - start_time
        print("Data was collected for {:.2f} seconds\n".format(execution_time))

    return wrapper


def start_threads(f):
    @functools.wraps(f)
    def wrapper(self):
        threads = f(self)
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        return threads

    return wrapper
