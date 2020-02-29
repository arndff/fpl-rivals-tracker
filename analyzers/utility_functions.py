from analyzers.MiniLeagueAnalyzer import MiniLeagueAnalyzer
from fileutils.FileUtils import FileUtils
from parsers.TeamDataParser import TeamDataParser


def read_ids(ids_file, league_id=-1, managers_count=-1):
    if league_id == -1:
        ids = FileUtils.read_ids_from_file(ids_file)
    else:
        page_standings = 1
        ids = []
        MiniLeagueAnalyzer(file_name="", league_id=league_id).extract_managers_ids(ids, page_standings)
        if managers_count > 0:
            ids = ids[:managers_count]

    return ids


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
        file_name = "{}_{}_gw{}".format(FileUtils.extract_file_name_from_path(ids_file), type_, current_event)
    else:
        file_name = league_name

    return output_path.format(file_name)

