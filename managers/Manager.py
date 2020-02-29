import threading


class Manager(threading.Thread):
    def __init__(self, team_id, current_event):
        threading.Thread.__init__(self)

        self._id = team_id
        self._current_event = current_event
