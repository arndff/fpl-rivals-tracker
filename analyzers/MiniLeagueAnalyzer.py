import csv
import time

from analyzers.HthAnalyzer import HthAnalyzer

from managers.Rival import Rival

from parsers.EventDataParser import EventDataParser
from parsers.LiveDataParser import LiveDataParser
from parsers.HthParser import HthParser
from parsers.TeamDataParser import TeamDataParser


class MiniLeagueAnalyzer:
    main_url = "https://fantasy.premierleague.com/api/"
    league_url = main_url + "leagues-classic/{}/standings/?page_new_entries={}&page_standings={}&phase={}"
    current_event = TeamDataParser(1).get_current_event()
    live_data_parser = LiveDataParser(current_event)

    ZARATA_LEAGUE_ID = 156718
    ELITE_64_LEAGUE_ID = 2379

    def __init__(self, league_id, file_name):
        self.__league_id = league_id
        self.__file_name = file_name
        (user, password) = HthAnalyzer.login()
        self.__session = HthParser.auth(user, password)

        start_time = time.time()

        if league_id != self.ZARATA_LEAGUE_ID:
            self.__managers_ids = []
        else:
            self.__managers_ids = [115, 21074, 99, 1908330, 503269]  # General, Sutherns, Will, Magnus, Dayvy

        self.__extract_managers_ids(1)
        self.__managers = self.__init_managers()

        self.__all_players_ids = self.__collect_players_ids()
        self.__all_players_names = self.__collect_players_data()

        self.__csv_data = self.__all_managers_to_list()

        execution_time = time.time() - start_time
        print("Data was collected for {:.2f} seconds".format(execution_time))

    def write_data_to_csv(self):
        filename = "csv/{}_gw{}.csv".format(self.__file_name, self.current_event)

        #headers = ["Manager Name",
        #           "Player 1", "Player 2", "Player 3", "Player 4", "Player 5", "Player 6",
        #           "Player 7", "Player 8", "Player 9", "Player 10", "Player 11",
        #           "Sub 1", "Sub 2", "Sub 3", "Sub 4"]

        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            #csvwriter.writerow(headers)
            csvwriter.writerows(zip(*self.__csv_data))

    def __extract_managers_ids(self, page_standings, page_new_entries=1, phase=1):
        formatted_url = self.league_url.format(self.__league_id, 1, page_standings, 1)
        self.__league_data = self.__session.get(formatted_url).json()
        has_next = self.__league_data["standings"]["has_next"]

        managers = self.__league_data["standings"]["results"]
        for manager in managers:
            self.__managers_ids.append(manager["entry"])

        if has_next:
            page_standings += 1
            self.__extract_managers_ids(page_standings)

    def __init_managers(self):
        threads = list(map(lambda id_: Rival(id_, self.current_event, False), self.__managers_ids))

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        return threads

    def __collect_players_ids(self):
        result = set()

        for manager in self.__managers:
            players_ids = manager.all_players_ids

            for player_id in players_ids:
                result.add(player_id)

        return result

    # this method returns a dictionary,
    # which values are: (player_name, player_points)
    def __collect_players_data(self):
        result = {}
        edp = EventDataParser(1, self.current_event)

        for player_id in self.__all_players_ids:
            result[player_id] = (edp.get_player_name(player_id),
                                 self.live_data_parser.get_player_points(player_id),
                                 edp.get_player_team(player_id))

        return result

    def __one_manager_to_list(self, manager, result):
        #result = [manager.manager_name]
        result[0].append(manager.manager_name)
        result[1].append("\n")
        result[2].append("\n")
        players_ids = manager.all_players_ids

        for player_id in players_ids:
            (player_name, player_points, player_team) = self.__all_players_names[player_id]

            if player_id == manager.captain_id:
                captain_points = self.live_data_parser.get_player_points(player_id)

                if manager.active_chip != "TC":
                    result[0].append(player_name + " (C)")
                    result[1].append(captain_points*2)
                else:
                    result[0].append(player_name + " (TC)")
                    result[1].append(captain_points*3)

            else:
                if player_id == manager.vice_captain_id:
                    result[0].append(player_name + " (VC)")
                else:
                    result[0].append(player_name)

                result[1].append(self.live_data_parser.get_player_points(player_id))

            result[2].append(player_team)

        [row.append("\n") for row in result]
        #return result

    def __all_managers_to_list(self):
        result = [[], [], []]

        for manager in self.__managers:
            #result.append(self.__manager_to_list(manager))
            self.__one_manager_to_list(manager, result)

        return result
