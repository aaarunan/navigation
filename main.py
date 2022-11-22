from GraphFileHandler import GraphFileHandler
import gc
import datetime
import Graph

GRAPH: Graph = None
PREPROCESS_TO: list = None
PREPROCESS_FROM: list = None

RECOURCES_DIR: str = "files"

EUROPA_LANDMARKS = [4248761, 6600989, 238502]
# euorpa_landmarks = [894067, 4248761, 2405345]
NODES_ISLAND = [[0, 10000]]
NODES_EUROPA = [[3292784, 7352330], [232073, 2518780], [7425499, 3430400]]
INTEREST_EUROPA = [
    [7172108, "vaernes", 4],
    [4546048, "trondheim_torg", 16],
    [3509663, "hemsedal", 8],
]
INTEREST_ISLAND = [[10000, "island-test", 4]]


def print_result(predecessors: list[int], time: float, nodes: int, length: int) -> None:
    if time is None:
        return
    print(f"time          {time:.4f}s")
    print(f"processed      {nodes} nodes")
    print(f"distance       {datetime.timedelta(seconds=int(length/100))}")
    print(f"nodes in path: {len(predecessors[0])}")


def read_preprocess(code: str, landmarks: int) -> None:
    directory = RECOURCES_DIR + "/" + code + "/preprocess"
    global PREPROCESS_FROM
    global PREPROCESS_TO
    PREPROCESS_FROM = GraphFileHandler.read_pre_process(
        directory + "/preprocess.alt.to", landmarks, GRAPH.nodes, debug=True
    )
    PREPROCESS_TO = GraphFileHandler.read_pre_process(
        directory + "/preprocess.alt.from", landmarks, GRAPH.nodes, debug=True
    )


def preprocess(
    code: str,
    landmarks: list[int],
) -> None:
    gc.disable()
    read_graph(code)
    gc.enable()
    directory = RECOURCES_DIR + "/" + code + "/preprocess"
    GraphFileHandler.pre_process(GRAPH, landmarks, directory)


def read_graph(code: str) -> None:
    global GRAPH
    directory = RECOURCES_DIR + "/" + code + "/data/"
    GRAPH = GraphFileHandler.graph_from_files(
        directory + "kanter.txt",
        directory + "noder.txt",
        directory + "interessepkt.txt",
        debug=True,
    )


def closest_interest(node: int, place: str, typ: int) -> None:
    gen = GRAPH.dijikstras(node, typ=typ)
    result = []
    for _ in range(8):
        result.append(next(gen))

    GraphFileHandler.make_csv(result, place)


def init(code: str) -> None:
    global GRAPH
    global PREPROCESS_FROM
    global PREPROCESS_TO

    # Improve performace by disabling garbage collection
    print("Disabling garbage collection")
    gc.disable()
    print("Loading graph...")
    read_graph(code)
    print("Reading preprocessed files...")
    read_preprocess(code, 3)
    print("Enabling garbage collection")
    gc.enable()
    gc.collect()


def pathfinding():
    loop = True
    while loop:
        try:
            start = int(input("start:"))
            stop = int(input("stop:"))
        except TypeError:
            print("Not a number.")
            pathfinding()
        data = GRAPH.alt(start, stop, PREPROCESS_FROM, PREPROCESS_TO)
        print_result(*data)

        data = next(GRAPH.dijikstras(start, stop=stop))
        print_result(*data)

        print("Writing result to file...")
        GraphFileHandler.make_csv(data[0][0], "out")
        del data
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
    pathfinding()


def test_all(code: str, nodes: list):
    init(code)
    for pair in nodes:
        from_node = pair[0]
        to_node = pair[1]
        for _ in range(2):
            print()
            print(f"From: {from_node} to: {to_node}")
            data_alt = GRAPH.alt(from_node, to_node, PREPROCESS_FROM, PREPROCESS_TO)
            print("ALT")
            print_result(*data_alt)
            data_dijikstra = next(GRAPH.dijikstras(from_node, typ=to_node))

            print("DIJIKSTRA")
            print_result(*data_dijikstra)
            from_node, to_node = to_node, from_node
    GraphFileHandler.make_csv(data_dijikstra[0][0], "test_all")
    del data_alt, data_dijikstra


# 1 Stedsnavn Trondheim, Moholt, …
# 2 Bensinstasjon Shell Herlev
# 4 Ladestasjon Ionity Klett
# 8 Spisested Restauranter, kafeer, puber
# 16 Drikkested Barer, puber, nattklubber
# 32 Overnattingssted Hoteller, moteller, gjestehus


def closest_all(code: str, interests: list):
    init(code)
    for interest in interests:
        closest_interest(*interest)


if __name__ == "__main__":
    # main()

    # test_all("europa", NODES_EUROPA)
    closest_all("europa", INTEREST_EUROPA)

    # test_all("island", NODES_ISLAND)
    # closest_all("island", INTEREST_ISLAND)

    # preprocess("europa", europa_landmarks)
    print("exiting...")
