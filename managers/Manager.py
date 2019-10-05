import threading


class Manager(threading.Thread):
    def __init__(self, id_, current_event):
        threading.Thread.__init__(self)

        self.id_ = id_
        self.current_event = current_event

        self.team_data_parser = None
        self.event_data_parser = None

        self.manager_name = ""

        [self.captain_id, self.vice_captain_id] = [0, 0]
        self.captain_name = self.vice_captain_name = ""

        self.players_ids = []

        self.active_chip = ""

    def __repr__(self):
        return self.manager_name
