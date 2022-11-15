from dataclasses import dataclass
from Graph import Graph
from Graph import Node
from gc import collect
import threading


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
    def pre_process_graph(graph: Graph, landmarks: list[int]) -> None:
        distances = graph.dijkstra_from_nodes(landmarks)
        GraphFileHandler._write_pre_process("preprocess.alt.to", distances)
        del distances
        collect()
        #Do this in another thread 
        #reverse_thread = threading.Thread()
        graph = graph.reverse()
        distances = graph.dijkstra_from_nodes(landmarks)
        GraphFileHandler._write_pre_process("preprocess.alt.from", distances)

    @staticmethod
    def read_pre_process(file_path: str):
        data = []
        with open(file_path, "r", encoding="UTF-8") as f:
            while line := f.readline():
                values = line.split()
                values = [int(x) for x in values]
                data.append(values[1:])
        return data

    @staticmethod
    def _write_pre_process(file_path: str, pre_process: list[list[int]]) -> None:
        with open(file_path, "w", encoding="UTF-8") as file:
            for index, entry in enumerate(pre_process):
                file.write(f"{index} ")
                for data in entry:
                    file.write(f"{data} ")
                file.write("\n")
