from dataclasses import dataclass
from Graph import Graph
from Graph import Node
import sys
import threading
from tqdm import tqdm


@dataclass
class LandMark:
    lon: float
    lat: float


class GraphFileHandler:
    @staticmethod
    def make_csv(predecessors: list[Node], file_name: str) -> None:
        with open(file_name + ".csv", "w", encoding="UTF-8") as file:
            file.write("value,lon,lat\n")
            for predecessor in predecessors:
                file.write(f"{predecessor.value},{predecessor.lon},{predecessor.lat}\n")

    @staticmethod
    def graph_from_files(
        file_path_edges: str, file_path_nodes: str, file_path_interest, debug=False
    ) -> Graph:
        with open(file_path_nodes, "r", encoding="UTF-8") as file_nodes:
            args = file_nodes.readline()
            args = args.split()
            graph = Graph(int(args[0]))
            if debug:
                print(f"Reading {file_path_edges}...")
                gen = tqdm(enumerate(file_nodes))
            else:
                gen = enumerate(file_nodes)
            for index, line in gen:
                values = line.split()
                graph.graph[index].lat = float(values[1])
                graph.graph[index].lon = float(values[2])

        if debug:
            print(f"Reading {file_path_nodes}...")
        with open(file_path_edges, "r", encoding="UTF-8") as file_edges:
            file_edges.readline()
            if debug:
                gen = tqdm(file_edges)
            else:
                gen = file_edges
            for line in gen:
                values = line.split()
                graph.add_connection(int(values[0]), int(values[1]), int(values[2]))

        if debug:
            print(f"Reading {file_path_interest}...")
        with open(file_path_interest, "r", encoding="UTF-8") as file_interest:
            file_interest.readline()
            if debug:
                gen = tqdm(file_interest)
            else:
                gen = file_interest
            for line in gen:
                values = line.split()
                graph.graph[int(values[0])].type = int(values[1])

        return graph

    @staticmethod
    def pre_process(graph: Graph, landmarks: list[int], directory: str, debug=True) -> None:
        GraphFileHandler._pre_process_graph(
            graph, landmarks, directory + "/preprocess.alt.to", silent = not debug
        )

        graph = graph.reverse()
        GraphFileHandler._pre_process_graph(
            graph, landmarks, directory + "/preprocess.alt.from", silent= not debug
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
    def _pre_process_graph(graph: Graph, landmarks: list[int], file_name: str, silent) -> None:
        for index, landmark in enumerate(landmarks):
            distances = graph.dijikstra_pre_process(landmark, silent=silent)
            GraphFileHandler._write_pre_process(f"{file_name}.{index}", distances)

        del distances

    @staticmethod
    def _pre_process_graph_multithreaded(
        graph: Graph, index: int, landmark: int, file_name: str
    ) -> None:
        distances = graph.dijikstra_pre_process(landmark)
        GraphFileHandler._write_pre_process(f"{file_name}.{index}", distances)

    @staticmethod
    def _write_pre_process(file_path: str, distances: list[int]) -> None:
        with open(file_path, "w", encoding="UTF-8") as file:
            for distance in distances:
                if distance == float("inf"):
                    distance = sys.maxsize
                file.write(f"{distance}\n")

    @staticmethod
    def read_pre_process(
        file_path: str, landmarks: int, nodes: int, debug: bool = False
    ) -> list[list[int]]:
        data = [[None] * landmarks for _ in range(nodes)]
        for i in range(landmarks):
            full_path = file_path + "." + str(i)
            if debug:
                print(f"Reading {full_path}...")
            with open(full_path, "r", encoding="UTF-8") as file:
                if debug:
                    gen = tqdm(enumerate(file))
                else:
                    gen = enumerate(file)
                for index, line in gen:
                    data[index][i] = int(line)
        return data
