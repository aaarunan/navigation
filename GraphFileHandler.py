from dataclasses import dataclass
from Graph import Graph
from Graph import Node
from gc import collect
import sys
import multiprocessing


@dataclass
class LandMark:
    lon: float
    lat: float


class GraphFileHandler:
    @staticmethod
    def make_csv(predecessors: list[Node]) -> None:
        with open("out.csv", "w", encoding="UTF-8") as file:
            file.write("value,lon,lat\n")
            for predecessor in predecessors:
                file.write(f"{predecessor.value},{predecessor.lon},{predecessor.lat}\n")

    @staticmethod
    def graph_from_files(file_path_edges: str, file_path_nodes: str) -> Graph:
        with open(file_path_edges, "r", encoding="UTF-8") as file_edges, open(
            file_path_nodes, "r", encoding="UTF-8"
        ) as file_nodes:
            file_edges.readline()
            args = file_nodes.readline()
            args = args.split()
            graph = Graph(int(args[0]), None)
            while line := file_edges.readline():
                values = line.split()
                graph.add(int(values[0]), int(values[1]), int(values[2]), None, None)

            while line := file_nodes.readline():
                values = line.split()
                node = int(values[0])
                if graph.graph[node] is None:
                    continue
                graph.graph[node].lat = float(values[1])
                graph.graph[node].lon = float(values[2])

            return graph

    @staticmethod
    def pre_process(graph: Graph, landmarks: list[int], dir: str) -> None:
        GraphFileHandler.pre_process_graph(graph, landmarks, dir + "/preprocess.alt.to")

        graph = graph.reverse()
        GraphFileHandler.pre_process_graph(graph, landmarks, dir + "/preprocess.alt.from")
    
    @staticmethod
    def pre_process_multithreaded(graph: Graph, landmarks: list[int], dir: str) -> None:

        #landmark = 0
        #GraphFileHandler.pre_process_graph(graph, [landmark], dir + f"/preprocess.alt.to.{landmark}")
        for index, landmark in enumerate(landmarks):
            multiprocessing.Process(target=GraphFileHandler.pre_process_graph_multithreaded, args=(graph, index, landmark, dir + "/preprocess.alt.to")).start()

        graph = graph.reverse()
        for index, landmark in enumerate(landmarks):
            multiprocessing.Process(target=GraphFileHandler.pre_process_graph_multithreaded, args=(graph, index, landmark, dir + "/preprocess.alt.from")).start()


    @staticmethod
    def pre_process_graph(graph: Graph, landmarks: list[int], file_name: str): 
        for index, landmark in enumerate(landmarks):
            distances = graph.dijikstra_from_node(landmark)
            GraphFileHandler._write_pre_process(
                f"{file_name}.{index}", distances
            )
        del distances
        collect()

    @staticmethod
    def pre_process_graph_multithreaded(graph: Graph, index:int ,landmark: int, file_name: str): 
            distances = graph.dijikstra_from_node(landmark)
            GraphFileHandler._write_pre_process(
                f"{file_name}.{index}", distances
            )

    @staticmethod
    def _write_pre_process(file_path: str, distances: list[int]) -> None:
        with open(file_path, "w", encoding="UTF-8") as file:
            for index, distance in enumerate(distances):
                if distance == float("inf"):
                    distance = sys.maxsize
                file.write(f"{index} {distance}\n")

    @staticmethod
    def read_pre_process(file_path: str, landmarks: int) -> list[list[int]]:
        data = []
        for i in range(landmarks):
            with open(file_path + "." + str(i), "r", encoding="UTF-8") as f:
                while line := f.readline():
                    values = line.split()
                    if i == 0:
                        data.append([int(values[1])])
                    else:
                        data[int(values[0])].append(int(values[1]))
        return data
