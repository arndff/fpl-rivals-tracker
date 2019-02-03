from headtohead.Analyzer import Analyzer


def execute():
    team_id = int(input("Enter your team ID: "))
    print("You're going to see your different players in each H2H match this GW. It'll take a few seconds...\n")
    analyzer = Analyzer(team_id)
    analyzer.print_all_matchups()


def main():
    execute()


if __name__ == "__main__":
    main()
