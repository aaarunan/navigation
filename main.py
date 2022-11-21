from GraphFileHandler import GraphFileHandler
import gc
import datetime
import Graph

GRAPH: Graph = None
PREPROCESS_TO: list = None
PREPROCESS_FROM: list = None
RECOURCES_DIR: str= "files"
EUROPE_LANDMARKS: int= 3
ISLAND_LANDMARKS: int = 3


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
    GraphFileHandler.pre_process(
        GRAPH,
        landmarks,
        directory
    )


def read_graph(code: str) -> None:
    global GRAPH
    directory = RECOURCES_DIR + "/" + code + "/data/"
    GRAPH = GraphFileHandler.graph_from_files(
        directory + "kanter.txt",
        directory + "noder.txt",
        directory + "interessepkt.txt",
        debug=True,
    )


def closest_interest(node: int, place: str, code: int) -> None:
    _, targets = GRAPH.dijikstra_all(node, code)
    result = []
    for _ in range(8):
        result.append(GRAPH.graph[targets.get()[1]])
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

        data = GRAPH.dijikstras(0, 100)

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


def test_island():
    init("island")
    from_node = 0
    to_node = 1000
    data_alt = GRAPH.alt(from_node, to_node, PREPROCESS_FROM, PREPROCESS_TO)
    print_result(*data_alt)
    data_dijikstra = GRAPH.dijikstras(from_node, stop=to_node)
    print_result(*data_dijikstra)

    print("Writing result to file...")
    GraphFileHandler.make_csv(data_alt[0][0], "test_island")

def test_all_island():
    init("island")
    nodes = [[0, 10000]]
    for pair in nodes:
        from_node = pair[0]
        to_node = pair[1]
        for _ in range(2):
            print()
            print(f"From: {from_node} to: {to_node}")
            data_alt = GRAPH.alt(from_node, to_node, PREPROCESS_FROM, PREPROCESS_TO)
            print("ALT")
            print_result(*data_alt)
            data_dijikstra = GRAPH.dijikstras(from_node, to_node)

            print("DIJIKSTRA")
            print_result(*data_dijikstra)
            from_node, to_node = to_node, from_node
            del data_alt
            del data_dijikstra
    #GraphFileHandler.make_csv(data_dijikstra[0][0], "test_all")

def test_all():
    init("europa")
    nodes = [[3292784, 7352330], [232073, 2518780], [7425499, 3430400]]
    for pair in nodes:
        from_node = pair[0]
        to_node = pair[1]
        for _ in range(2):
            print()
            print(f"From: {from_node} to: {to_node}")
            data_alt = GRAPH.alt(from_node, to_node, PREPROCESS_FROM, PREPROCESS_TO)
            print("ALT")
            print_result(*data_alt)
            data_dijikstra = GRAPH.dijikstras(from_node, to_node)

            print("DIJIKSTRA")
            print_result(*data_dijikstra)
            from_node, to_node = to_node, from_node
            del data_alt
            del data_dijikstra
    GraphFileHandler.make_csv(data_dijikstra[0][0], "test_all")


def closest_all():
    # 1 Stedsnavn Trondheim, Moholt, …
    # 2 Bensinstasjon Shell Herlev
    # 4 Ladestasjon Ionity Klett
    # 8 Spisested Restauranter, kafeer, puber
    # 16 Drikkested Barer, puber, nattklubber
    # 32 Overnattingssted Hoteller, moteller, gjestehus
    init("europa")
    closest_interest(7172108, "vaernes", 4)
    closest_interest(4546048, "trondheim_torg", 16)
    closest_interest(3509663, "hemsedal", 8)


europa_nodes = [4248761, 6600989, 238502]
if __name__ == "__main__":
    #test_all()
    #closest_all()
    # main()
    #test_island()
    test_all_island() 
    #preprocess("europa", europa_nodes)
    print("exiting...")
