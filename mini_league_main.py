from analyzers.MiniLeagueAnalyzer import MiniLeagueAnalyzer


def read_league_id():
    league_id = -1

    while league_id == -1:
        try:
            league_id = int(input("Enter league's ID: "))
        except ValueError:
            print("Please enter a valid integer! Try again.\n")

    return league_id


def read_file_name():
    file_name = input("Enter file's name: ")
    print()

    return file_name


def main():
    league_id = read_league_id()
    file_name = read_file_name()

    mla = MiniLeagueAnalyzer(league_id, file_name)
    mla.write_data_to_csv()


if __name__ == "__main__":
    main()
