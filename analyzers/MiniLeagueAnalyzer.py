import csv
from pathlib import Path

from analyzers.utility_functions import get_current_event, start_threads, \
                                        extract_teams_ids_from_league, read_ids_from_file
from fileutils.fileutils import extract_file_name_from_path
from managers.ClassicManager import ClassicManager

from parsers.EventDataParser import EventDataParser
from parsers.LiveDataParser import LiveDataParser


class MiniLeagueAnalyzer:
    __current_event = get_current_event()
    __live_data_parser = LiveDataParser(__current_event)

    __ZARATA_LEAGUE_ID = 156718
    __ELITE_64_LEAGUE_ID = 2379

    __DEFAULT_SAVE_PATH = "csv"

    def __init__(self, ids_file, save_dir="", league_name="", league_id=-1):
        self.__managers_ids = self.__load_ids(league_id, ids_file)
        self.__config_zarata(league_id)
        self.__managers = self.__init_managers()

        self.__all_players_ids = self.__collect_players_ids()
        self.__all_players_names = self.__collect_players_data()

        self.__csv_data = self.__all_managers_to_list()

        [self.__save_dir, self.__save_path] = self.__set_save_path(ids_file, save_dir, league_name, league_id)

    def write_data_to_csv(self):
        # headers = ["Manager Name",
        #            "Player 1", "Player 2", "Player 3", "Player 4", "Player 5", "Player 6",
        #            "Player 7", "Player 8", "Player 9", "Player 10", "Player 11",
        #            "Sub 1", "Sub 2", "Sub 3", "Sub 4"]

        Path(self.__save_dir).mkdir(parents=True, exist_ok=True)
        with open(self.__save_path, "w", newline="\n", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            #csvwriter.writerow(headers)
            csvwriter.writerows(zip(*self.__csv_data))

    def __load_ids(self, league_id, ids_file):
        if league_id == -1:
            managers_ids = read_ids_from_file(ids_file)
        else:
            managers_ids = extract_teams_ids_from_league(league_id)

        # managers_ids = read_ids_from_file(ids_file) if league_id == -1 else extract_teams_ids_from_league(league_id)
        return managers_ids

    def __config_zarata(self, league_id):
        if league_id == self.__ZARATA_LEAGUE_ID:
            self.__managers_ids.sort()
            self.__managers_ids_sorted = self.__managers_ids

            self.__managers_ids = [115, 21074, 99, 1908330, 503269]  # General, Sutherns, Will, Magnus, Dayvy

            for id_ in self.__managers_ids_sorted:
                self.__managers_ids.append(id_)

    @start_threads
    def __init_managers(self):
        threads = list(map(lambda id_: ClassicManager(id_, self.__current_event), self.__managers_ids))
        return threads

    def __collect_players_ids(self):
        result = set()

        for manager in self.__managers:
            players_ids = manager.all_players_ids

            for player_id in players_ids:
                result.add(player_id)

        return result

    """
    This method returns a dictionary,
    which values are: (player_name, player_points)
    """
    def __collect_players_data(self):
        result = {}
        event_data_parser = EventDataParser(1, self.__current_event)

        for player_id in self.__all_players_ids:
            result[player_id] = (event_data_parser.get_player_name(player_id),
                                 self.__live_data_parser.get_player_points(player_id),
                                 event_data_parser.get_player_team(player_id))

        return result

    def __one_manager_to_list(self, manager, result):
        #result = [manager.manager_name]
        result[0].append(manager.manager_name)
        #manager.format_gw_points()
        #result[1].append(manager.gw_points_string)
        result_length = len(result)
        for i in range(1, result_length):
            result[i].append("\n")

        players_ids = manager.all_players_ids

        for player_id in players_ids:
            (player_name, player_points, player_team) = self.__all_players_names[player_id]

            if player_id == manager.captain_id:
                captain_points = self.__live_data_parser.get_player_points(player_id)

                if manager.active_chip != "TC":
                    result[0].append(player_name)
                    result[1].append(captain_points*2)
                    result[2].append("C")
                else:
                    result[0].append(player_name)
                    result[1].append(captain_points*3)
                    result[2].append("TC")

            else:
                if player_id == manager.vice_captain_id:
                    result[0].append(player_name)
                    result[2].append("VC")
                else:
                    result[0].append(player_name)
                    result[2].append("-")

                result[1].append(self.__live_data_parser.get_player_points(player_id))

            result[3].append(player_team)

        [row.append("\n") for row in result]
        #return result

    def __all_managers_to_list(self):
        # col 1: players' names
        # col 2: players' points
        # col 3: - / c / vc
        # col 4: players' teams

        result = [[], [], [], []]

        for manager in self.__managers:
            #result.append(self.__manager_to_list(manager))
            self.__one_manager_to_list(manager, result)

        return result

    def __set_save_path(self, ids_file, save_dir, league_name, league_id):
        save_dir = self.__DEFAULT_SAVE_PATH if save_dir == "" else save_dir
        csv_filename = league_name if league_id != -1 else extract_file_name_from_path(ids_file)
        save_path = "{}/{}_gw{}.csv".format(save_dir, csv_filename, self.__current_event)

        result = (save_dir, save_path)
        return result
