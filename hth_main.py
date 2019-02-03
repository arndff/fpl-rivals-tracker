from headtohead.ManipulateHthData import ManipulateHthData


def execute():
    team_id = int(input("Enter your team ID: "))
    print("You're going to see your different players in each H2H match this GW. It'll take a few seconds...\n")
    obj = ManipulateHthData(team_id)
    obj.print_all_matchups()


def main():
    execute()


if __name__ == "__main__":
    main()
