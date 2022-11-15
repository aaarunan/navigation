from GraphFileHandler import GraphFileHandler

GRAPH = None
PREPROCESS_TO = None
PREPROCESS_FROM = None


# GraphFileHandler.pre_process_graph(graph, [22864, 0, 109910])
# GraphFileHandler.pre_process_graph(graph, [2151398, 1236417, 3225427])


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
        "files/island/preprocess/preprocess.alt.from"
    )
    PREPROCESS_TO = GraphFileHandler.read_pre_process(
        "files/island/preprocess/preprocess.alt.to"
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
        "files/europa/preprocess/preprocess.alt.from"
    )
    PREPROCESS_TO = GraphFileHandler.read_pre_process(
        "files/europa/preprocess/preprocess.alt.to"
    )


def main():
    init_europe()
    find_path_alt_europa()
    print("exiting...")


if __name__ == "__main__":
    main()
