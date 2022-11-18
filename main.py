from GraphFileHandler import GraphFileHandler

GRAPH = None
PREPROCESS_TO = None
PREPROCESS_FROM = None
RECOURCES_DIR = "files"
EUROPE_LANDMARKS = 3


def print_result(time, nodes, distances, length):
    print(f"done. ({time})")
    print(f"processed      {nodes} nodes")
    print(f"distance       {length/100/60/60} timer")
    print(f"Nodes in path: {len(distances[0])}")


def read_preprocess(
    code: str,
    landmarks: int
):
    directory = RECOURCES_DIR + "/" + code + "/preprocess"
    global PREPROCESS_FROM
    global PREPROCESS_TO
    PREPROCESS_FROM = GraphFileHandler.read_pre_process(directory + "/preprocess.alt.from", landmarks)
    PREPROCESS_TO = GraphFileHandler.read_pre_process(directory +  "/preprocess.alt.from", landmarks)


def preprocess(
    code: str,
    landmarks: list[int],
):
    GraphFileHandler.pre_process(GRAPH, landmarks, RECOURCES_DIR + code)


def read_graph(code: str):
    global GRAPH
    directory = RECOURCES_DIR + "/" + code + "/data/"
    GRAPH = GraphFileHandler.graph_from_files(directory + "kanter.txt", directory + "noder.txt", directory + "interessepkt.txt")

def init(code: str):
    global GRAPH
    global PREPROCESS_FROM
    global PREPROCESS_TO

    print("Loading graph")
    read_graph(code)
    read_preprocess(code, 3)

def test_trondheim():
    init("europa")
    from_node = 7425499
    to_node = 3430400
    predecessors, time, nodes, length = GRAPH.alt(
        from_node, to_node, PREPROCESS_TO, PREPROCESS_FROM
    )
    print_result(time, nodes, predecessors, length)
    predecessors, time, nodes, length = GRAPH.dijikstras(from_node, to_node)

    print_result(time, nodes, predecessors, length)

def test_island():
    init("island")
    from_node = 0 
    to_node = 100
    predecessors, time, nodes, length = GRAPH.alt(
        from_node, to_node, PREPROCESS_TO, PREPROCESS_FROM
    )
    predecessors, time, nodes, length = GRAPH.dijikstras(from_node, to_node)

    print_result(time, nodes, predecessors, length)

    print("Writing result to file...")
    GraphFileHandler.make_csv(predecessors[0])



def main_patfinding():
    loop = True
    while loop:
        try:
            start = int(input("start:"))
            stop = int(input("stop:"))
        except TypeError:
            print("Not a number.")
            main_patfinding()
        predecessors, time, nodes, length = GRAPH.alt(
            start, stop, PREPROCESS_TO, PREPROCESS_FROM
        )
        print_result(time, nodes, predecessors, length)

        predecessors, time, nodes, length = GRAPH.dijikstras(0, 100)

        print("Writing result to file...")
        GraphFileHandler.make_csv(predecessors[0])
        option = input("Continue with other nodes? [Y/n] ")
        if option == "n":
            loop = False


def main():
    print("1. europe")
    print("2. iceland")
    print("3. pre process europe")
    print("4. pre process iceland")
    try:
        option = int(input("Choose and option: "))
    except TypeError:
        print("Not a number.")
        main()

    match (option):
        case 1:
            init("europa")
        case 2:
            init("island")
        case 3:
            preprocess("europa", None)
        case 4:
            preprocess("island", None)
        case _:
            print("Not a valid option.")
            main()
    main_patfinding()

    print("exiting...")


if __name__ == "__main__":
    main()
