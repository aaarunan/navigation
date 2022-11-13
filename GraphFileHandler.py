from dataclasses import dataclass
from Graph import Graph
import tqdm
import gc

@dataclass
class LandMark:
    lon: float
    lat: float
   
class GraphFileHandler:

    @staticmethod
    def read_landmarks(file_path: str) -> list[int]:
        landmarks = []
        with open(file_path, 'r', encoding='UTF-8') as file:
            file.readline()
            while line := file.readline():
                values = line.split()
                landmarks.append(LandMark(float(values[2]), float(values[1])))
        return landmarks

    @staticmethod
    def make_csv(predecessors: list[int], landmarks: list[LandMark]) -> None:
        with open("out.csv", "w", encoding="UTF-8") as file:
            file.write("value,lon,lat\n")
            for predecessor in predecessors:
                landmark = landmarks[predecessor]
                file.write(f"{predecessor},{landmark.lon},{landmark.lat}\n")

    @staticmethod
    def load_from_file(file_path: str) -> Graph:
        print("parsing file...")
        with open(file_path, "r", encoding="UTF-8") as file:
            args = file.readline()
            args = args.split()
            graph = Graph(7509994, None)
            while line := file.readline():
                values = line.split()
                graph.add(int(values[0]), int(values[1]), int(values[2]))
            return graph


    @staticmethod
    def pre_process_graph(graph: Graph, landmarks: list[int]) -> None:
        distances = graph.dijkstra_all_nodes_from_landmarks(landmarks)
        GraphFileHandler._write_pre_process("preprocess.alt.to", distances)
        del distances
        gc.collect()
        graph = graph.reverse()
        distances = graph.dijkstra_all_nodes_from_landmarks(landmarks)
        GraphFileHandler._write_pre_process("preprocess.alt.from", distances)
    
        
    @staticmethod
    def _write_pre_process(file_path: str, pre_process: list[list[int]]) -> None:
        with open(file_path, "w", encoding="UTF-8") as file:
            for index, entry in enumerate(pre_process):
                file.write(f"{index} ")
                for data in entry:
                    file.write(f"{data} ")
                file.write("\n")

                
