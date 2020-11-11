def load_data(path):
    # Return some processed data for purpose of demo
    # Marker "X" used instead of the default "A" to demonstrate renaming
    return [{"X": 1, "B": 5, "C": 4},
            {"X": 2, "B": 4, "C": 6},
            {"X": 3, "B": 1, "C": 9}]


def write_data(path, results):
    with open(path, "w") as f:
        f.write(results)
