from analyzers.CaptainPicksAnalyzer import CaptainPickAnalyzer
from read_input import read_input


def execute():
    team_id = read_input("Enter team ID: ")
    captain_picks_analyzer = CaptainPickAnalyzer(team_id)
    captain_picks_analyzer.print_table()


def main():
    execute()


if __name__ == "__main__":
    main()
