from GraphFileHandler import GraphFileHandler


print("parsing graph")
graph = GraphFileHandler.graph_from_files("files/island/kanter.txt", "files/island/noder.txt")

#GraphFileHandler.pre_process_graph(graph, [22864, 0, 109910])
#GraphFileHandler.pre_process_graph(graph, [2151398, 1236417, 3225427])

print("Reading pre process files")
preprocess_from = GraphFileHandler.read_pre_process("files/preprocess/island/preprocess.alt.from")
preprocess_to = GraphFileHandler.read_pre_process("files/preprocess/island/preprocess.alt.to")

from_node = 66617
to_node = 107848
predecessors, distance = graph.alt(from_node, to_node, preprocess_from, preprocess_to)
predecessors, distance = graph.dijikstras(from_node, to_node)


print("Writing result to file...")
GraphFileHandler.make_csv(predecessors)
#print("done.")
