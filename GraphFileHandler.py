from dataclasses import dataclass
from Graph import Graph
from Graph import Node
import gc
import sys
import threading
from tqdm import tqdm


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
        #Improve performace by disabling garbage collection
        #This is due to append being slow when appending objects
        gc.disable()
        with open(file_path_nodes, "r", encoding="UTF-8") as file_nodes:
            args = file_nodes.readline()
            args = args.split()
            graph = Graph(int(args[0]), None)

        with open(file_path_edges, "r", encoding="UTF-8") as file_edges:
            file_edges.readline()
            for line in tqdm(file_edges):
                values = line.split()
                graph.add(int(values[0]), int(values[1]), int(values[2]), None, None)

        with open(file_path_nodes, "r", encoding="UTF-8") as file_nodes:
            file_nodes.readline()
            for line in tqdm(file_nodes):
                values = line.split()
                node = int(values[0])
                if graph.graph[node] is None:
                    continue
                graph.graph[node].lat = float(values[1])
                graph.graph[node].lon = float(values[2])
        print("Enabling garbage collection")
        gc.enable()

        return graph

    @staticmethod
    def pre_process(graph: Graph, landmarks: list[int], directory: str) -> None:
        GraphFileHandler._pre_process_graph(
            graph, landmarks, directory + "/preprocess.alt.to"
        )

        graph = graph.reverse()
        GraphFileHandler._pre_process_graph(
            graph, landmarks, directory + "/preprocess.alt.from"
        )

    @staticmethod
    def pre_process_multithreaded(
        graph: Graph, landmarks: list[int], directory: str
    ) -> None:

        for index, landmark in enumerate(landmarks):
            threading.Thread(
                target=GraphFileHandler._pre_process_graph_multithreaded,
                args=(graph, index, landmark, directory + "/preprocess.alt.to"),
            ).start()

        graph = graph.reverse()
        for index, landmark in enumerate(landmarks):
            threading.Thread(
                target=GraphFileHandler._pre_process_graph_multithreaded,
                args=(graph, index, landmark, directory + "/preprocess.alt.from"),
            ).start()

    @staticmethod
    def _pre_process_graph(graph: Graph, landmarks: list[int], file_name: str):
        for index, landmark in enumerate(landmarks):
            distances = graph.dijikstra_from_node(landmark)
            GraphFileHandler._write_pre_process(f"{file_name}.{index}", distances)

        del distances
        gc.collect()

    @staticmethod
    def _pre_process_graph_multithreaded(
        graph: Graph, index: int, landmark: int, file_name: str
    ):
        distances = graph.dijikstra_from_node(landmark)
        GraphFileHandler._write_pre_process(f"{file_name}.{index}", distances)

    @staticmethod
    def _write_pre_process(file_path: str, distances: list[int]) -> None:
        with open(file_path, "w", encoding="UTF-8") as file:
            for distance in distances:
                if distance == float("inf"):
                    distance = sys.maxsize
                file.write(f"{distance}\n")


    @staticmethod
    def read_pre_process(file_path: str, landmarks: int) -> list[list[int]]:
        gc.disable()
        data = []
        for i in range(landmarks):
            index = 0
            with open(file_path + "." + str(i), "r", encoding="UTF-8") as f:
                for line in tqdm(f):
                    if i == 0:
                        data.append([int(line)])
                    else:
                        data[index].append(int(line))
                    index += 1
        gc.enable()
        gc.collect()
        return data
