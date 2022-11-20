from GraphFileHandler import GraphFileHandler
import gc
import datetime
import Graph

GRAPH: Graph = None
PREPROCESS_TO = None
PREPROCESS_FROM = None
RECOURCES_DIR = "files"
EUROPE_LANDMARKS = 3
ISLAND_LANDMARKS = 3


def print_result(predecessors, time, nodes, length):
    if time is None:
        return
    print(f"time          {time:.4f}s")
    print(f"processed      {nodes} nodes")
    print(f"distance       {datetime.timedelta(seconds=int(length/100))}")
    print(f"nodes in path: {len(predecessors[0])}")


def read_preprocess(code: str, landmarks: int):
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
):
    read_graph(code)
    GraphFileHandler.pre_process(
        GRAPH, landmarks, RECOURCES_DIR + "/" + code + "/preprocess"
    )


def read_graph(code: str):
    global GRAPH
    directory = RECOURCES_DIR + "/" + code + "/data/"
    GRAPH = GraphFileHandler.graph_from_files(
        directory + "kanter.txt",
        directory + "noder.txt",
        directory + "interessepkt.txt",
        debug=True,
    )


def init(code: str):
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
        GraphFileHandler.make_csv(data[0][0], str(start) + "-" + str(stop))
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


def test_all():
    init("europa")
    nodes = [[3292784, 7352330], [232073, 2518780]]
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
    GraphFileHandler.make_csv(data_dijikstra[0][0], "test_all")

def closest_from_to_place(node: int, place: str, code: int):
    _, targets = GRAPH.dijikstra_all(node, code)
    result = []
    for _ in range(8):
        result.append(GRAPH.graph[targets.get()[1]])
    GraphFileHandler.make_csv(result, place)


def test_island():
    init("island")
    from_node = 0
    to_node = 100
    data_alt = GRAPH.alt(from_node, to_node, PREPROCESS_FROM, PREPROCESS_TO)
    print_result(*data_alt)
    data_dijikstra = GRAPH.dijikstras(from_node, stop=to_node)
    print_result(*data_dijikstra)

    print("Writing result to file...")
    GraphFileHandler.make_csv(data_alt[0][0], "test_island")

def closest_all():
    #1 Stedsnavn Trondheim, Moholt, …
    #2 Bensinstasjon Shell Herlev
    #4 Ladestasjon Ionity Klett
    #8 Spisested Restauranter, kafeer, puber
    #16 Drikkested Barer, puber, nattklubber
    #32 Overnattingssted Hoteller, moteller, gjestehus
    init("europa")
    closest_from_to_place(7172108, "vaernes", 4)
    closest_from_to_place(4546048, "trondheim_torg", 16)
    closest_from_to_place(3509663, "hemsedal", 8)

europa_nodes = [4248761, 6600989, 238502]
if __name__ == "__main__":
    #test_all()
    closest_all()
    #main()
    
    #preprocess("europa", europa_nodes)
    print("exiting...")
