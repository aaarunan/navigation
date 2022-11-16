from dataclasses import dataclass
from Graph import Graph
from Graph import Node
from gc import collect
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
        with open(file_path_nodes, "r", encoding="UTF-8") as file_nodes:
            args = file_nodes.readline()
            args = args.split()
            graph = Graph(int(args[0]), None)

        with open(file_path_edges, "r", encoding="UTF-8") as file_edges:
            pbar = tqdm(total=int(file_edges.readline()))

            while line := file_edges.readline():
                pbar.update(1)
                values = line.split()
                graph.add(int(values[0]), int(values[1]), int(values[2]), None, None)

        with open(file_path_nodes, "r", encoding="UTF-8") as file_nodes:
            file_nodes.readline()
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
        GraphFileHandler._pre_process_graph(
            graph, landmarks, dir + "/preprocess.alt.to"
        )

        graph = graph.reverse()
        GraphFileHandler._pre_process_graph(
            graph, landmarks, dir + "/preprocess.alt.from"
        )

    @staticmethod
    def pre_process_multithreaded(
        graph: Graph, landmarks: list[int], directory: str
    ) -> None:

        # landmark = 0
        # GraphFileHandler.pre_process_graph(graph, [landmark], dir + f"/preprocess.alt.to.{landmark}")
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
        collect()

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
        data = []
        for i in range(landmarks):
            index = 0
            with open(file_path + "." + str(i), "r", encoding="UTF-8") as f:
                while line := f.readline():
                    value = int(line)
                    if i == 0:
                        data.append([value])
                    else:
                        data[index].append(value)
                    index += 1
        return data
