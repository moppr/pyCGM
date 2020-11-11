def load_data(path):
    #with open(path) as f:
        # return f.read().split(",")
    return [{"A": 1, "B": 4}, {"A": 2, "B": 6}, {"A": 3, "B": 10}]

def write_data(path, results):
    with open(path, "w") as f:
        f.write(results)