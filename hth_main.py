from analyzers.HthAnalyzer import HthAnalyzer


def execute():
    team_id = int(input("Enter your team ID: "))
    print("You're going to see your different players in each H2H match this GW. It'll take a few seconds...\n")
    hth_analyzer = HthAnalyzer(team_id)
    hth_analyzer.print_all_matchups()

    print("Good luck, {}! :)".format(hth_analyzer.manager_name))


def main():
    execute()


if __name__ == "__main__":
    main()
