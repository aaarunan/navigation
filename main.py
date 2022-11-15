from GraphFileHandler import GraphFileHandler

GRAPH = None
PREPROCESS_TO = None
PREPROCESS_FROM = None


def preprocess_island():
    global GRAPH


    GRAPH = GraphFileHandler.graph_from_files(
        "files/island/data/kanter.txt", "files/island/data/noder.txt"
    )
    GraphFileHandler.pre_process(GRAPH, [22864, 0, 109910], "files/island/preprocess")


def preprocess_island_multithreaded():
    global GRAPH

    GRAPH = GraphFileHandler.graph_from_files(
        "files/island/data/kanter.txt", "files/island/data/noder.txt"
    )
    GraphFileHandler.pre_process_multithreaded(GRAPH, [22864, 0, 109910], "files/island/preprocess")


def preprocess_europe():
    global GRAPH
    
    GRAPH = GraphFileHandler.graph_from_files(
        "files/europa/data/kanter.txt", "files/europa/data/noder.txt"
    )
    GraphFileHandler.pre_process(
        GRAPH, [2151398, 1236417, 3225427], "files/europa/preprocess"
    )

def preprocess_europe_multithreaded():
    global GRAPH
    
    GRAPH = GraphFileHandler.graph_from_files(
        "files/europa/data/kanter.txt", "files/europa/data/noder.txt"
    )
    GraphFileHandler.pre_process_multithreaded(
        GRAPH, [2151398, 1236417, 3225427], "files/europa/preprocess"
    )

def find_path_island_test():
    from_node = 66617
    to_node = 104855
    GRAPH.alt(from_node, to_node, PREPROCESS_FROM, PREPROCESS_TO)
    GRAPH.dijikstras(from_node, to_node)


def find_path_alt_island():
    from_node = 66617
    to_node = 104855
    predecessors, _ = GRAPH.alt(from_node, to_node, PREPROCESS_FROM, PREPROCESS_TO)

    print("Writing result to file...")
    GraphFileHandler.make_csv(predecessors)


def find_path_alt_europa():
    from_node = 6684812
    to_node = 3430400
    predecessors, _ = GRAPH.alt(from_node, to_node, PREPROCESS_FROM, PREPROCESS_TO)

    print("Writing result to file...")
    GraphFileHandler.make_csv(predecessors)


def init_island():
    global GRAPH
    global PREPROCESS_FROM
    global PREPROCESS_TO

    print("Loading graph")
    GRAPH = GraphFileHandler.graph_from_files(
        "files/island/data/kanter.txt", "files/island/data/noder.txt"
    )

    print("Loading preprocess files")
    PREPROCESS_FROM = GraphFileHandler.read_pre_process(
        "files/island/preprocess/preprocess.alt.from", 3
    )
    PREPROCESS_TO = GraphFileHandler.read_pre_process(
        "files/island/preprocess/preprocess.alt.to", 3
    )


def init_europe():
    global GRAPH
    global PREPROCESS_FROM
    global PREPROCESS_TO

    print("Loading graph")
    GRAPH = GraphFileHandler.graph_from_files(
        "files/europa/data/kanter.txt", "files/europa/data/noder.txt"
    )

    print("Loading preprocess files")
    PREPROCESS_FROM = GraphFileHandler.read_pre_process(
        "files/europa/preprocess/preprocess.alt.from", 2
    )
    PREPROCESS_TO = GraphFileHandler.read_pre_process(
        "files/europa/preprocess/preprocess.alt.to", 2
    )


def main():
    print("Loading graph")
    ##### europa #####

    preprocess_europe_multithreaded()

    # init_europe()
    # find_path_alt_europa()

    ##### island ######

    #preprocess_island_multithreaded()
    #preprocess_island()

    #init_island()
    #find_path_alt_island()

    print("exiting...")


if __name__ == "__main__":
    main()
