def read_input(msg):
    id_ = -1

    while id_ == -1:
        try:
            id_ = int(input(msg))
        except ValueError:
            print("Please enter a valid integer! Try again.\n")

    return id_
