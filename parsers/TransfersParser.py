import sys

from parsers.Parser import Parser


class TransfersParser(Parser):
    __UPDATE_MSG = "The game is being updated."

    def __init__(self, id_, gw, event_data_parser, live_data_parser):
        super().__init__(id_)
        self.__id_ = id_
        self.__gw = gw
        self.__event_data_parser = event_data_parser
        self.__live_data_parser = live_data_parser

        self.__data = super()._get_url_data("transfers")

        if self.__data == self.__UPDATE_MSG:
            print("The game is being updated.")
            print("Please try again later when the updated scores / teams will be available.")
            sys.exit(1)

    def get_transfers(self):
        transferred_players = self.__get_transferred_players_names()
        transfers = []

        if len(transferred_players) == 0:
            result = ["None", "None", 0, 0]
            return result

        (players_points, sold_players_points, bought_players_points) = self.__get_transferred_players_points()

        # [(("Vardy","Aguero"), (5, 10)), ...]
        names_and_points = zip(self.__get_transferred_players_names(),
                               players_points)

        for transfer in names_and_points:
            transfers.append(("{}:{}".format(transfer[0][0], transfer[1][0]),
                              "{}:{}".format(transfer[0][1], transfer[1][1])))

        sold_players = []
        bought_players = []

        for transfer in transfers:
            sold_players.append(transfer[0])
            bought_players.append(transfer[1])

        # sold_players, bought_players are strings
        result = (', '.join(sold_players), ', '.join(bought_players), sold_players_points, bought_players_points)
        return result

    def __get_transferred_players_points(self):
        transfers_ids = self.__get_transfers_ids_current_gw()
        points = []

        if len(transfers_ids) == 0:
            return points

        for transfer in transfers_ids:
            transfer_out_points = self.__live_data_parser.get_player_points(transfer[0])
            transfer_in = transfer[1]
            transfer_in_points = self.__live_data_parser.get_player_points(transfer[1])

            if transfer_in == self.__event_data_parser.get_captains_id()[0]:
                if "TC" == self.__event_data_parser.get_active_chip():
                    transfer_in_points += 2*transfer_in_points
                else:
                    transfer_in_points += transfer_in_points

            current_transfer = (transfer_out_points, transfer_in_points)
            points.append(current_transfer)

        sold_players_points = -1
        bought_players_points = -1

        for pair in points:
            sold_players_points += pair[0]
            bought_players_points += pair[1]

        result = (points, sold_players_points, bought_players_points)
        return result

    def __get_transferred_players_names(self):
        transfers_ids = self.__get_transfers_ids_current_gw()
        transferred_players_names = []

        if len(transfers_ids) == 0:
            return transferred_players_names

        for transfer in transfers_ids:
            transfer_out_name = self.__event_data_parser.get_player_name(transfer[0])

            transfer_in = transfer[1]
            transfer_in_name = self.__event_data_parser.get_player_name(transfer[1])

            if transfer_in == self.__event_data_parser.get_captains_id()[0]:
                if "TC" == self.__event_data_parser.get_active_chip():
                    transfer_in_name += " (TC)"
                else:
                    transfer_in_name += " (C)"

            players_names = (transfer_out_name, transfer_in_name)
            transferred_players_names.append(players_names)

        return transferred_players_names

    def __get_transfers_ids_current_gw(self):
        transfers_ids = []

        # if len(self.__data) == 0:
        #    return transfers_ids

        for transfer in self.__data:
            if transfer["event"] == self.__gw:
                transfer_ids = (transfer["element_out"], transfer["element_in"])
                transfers_ids.append(transfer_ids)

        return transfers_ids
