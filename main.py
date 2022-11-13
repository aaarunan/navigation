from Graph import Graph
from GraphFileHandler import GraphFileHandler


graph = GraphFileHandler.load_from_file("files/europa/kanter.txt")

#GraphFileHandler.pre_process_graph(graph, [78395, 20661])

#predecessors, distance = graph.dijikstras(78395, 20661)
#landmarks = GraphFileHandler.read_landmarks("files/island/noder.txt")
#GraphFileHandler.make_csv(predecessors, landmarks)

