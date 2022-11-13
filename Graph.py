from dataclasses import dataclass
import tqdm
from PriorityQueue import PriorityQueue

@dataclass
class Edge:
    start: int
    end: int
    weight: int


@dataclass
class Node:
    value: int
    edges: list[Edge]
    lon: float
    lat: float
    distance_alt: int = None

    def append_edge(self, end: int, weight: int) -> None:
        self.edges.append(Edge(self.value, end, weight))


class Graph:
    nodes: int
    edges: list[Edge]
    graph: list[Node]
    

    def __init__(self, nodes: int, edges: list[Edge]) -> None:
        self.nodes = nodes
        self.edges = edges
        self.graph = [None] * self.nodes


    def add(self, start: int, end: int, weight: int, lon: float, lat: float) -> None:
        if self.graph[start] is not None:
            self.graph[start].append_edge(end, weight)
            return
        self.graph[start] = Node(start, [Edge(start, end, weight)], lon, lat)

    def dijikstras(self, start: int, stop: int = None, only_distances: bool = False):
        distances = [[None, float("inf")]] * self.nodes
        distances[start] = ["start", 0]
        queue = PriorityQueue()
        queue.insert(self.graph[start].value, 0)

        visited = [False] * self.nodes
        #pbar = tqdm.tqdm(total=self.nodes)
        #print("Finding paths...")
        while queue.length != 0:
            index, distance = queue.peek()
            current_node = self.graph[index]
            
            if stop is not None and index == stop:
                break
            
            if current_node is None:
                continue
            if visited[index]:
                continue
            #pbar.update(1)
            visited[index] = True
            distances[current_node.value][1] = distance

            for edge in current_node.edges:
                if visited[edge.end]:
                    continue
                new_weight = distance + edge.weight
                if new_weight < distances[edge.end][1]:
                    queue.insert(edge.end, new_weight)
                    distances[edge.end] = [edge.start, new_weight]

        if stop is None:
            return distances
        if only_distances:
            return distances[stop][1]
        return self.get_predecessors(distances, start, stop)
    
    def alt(self):
        pass

        
    def dijkstra_all_nodes_from_landmarks(self, landmarks) -> list[list[int]]:
        pre_process = [([None] * len(landmarks))[:] for _ in range(self.nodes)]

        pbar = tqdm.tqdm(total=self.nodes * len(landmarks))

        for i, landmark in enumerate(landmarks):
            distances = self.dijikstras(landmark, only_distances=True)
            for j, distance in enumerate(distances):
                temp = distance[1]
                pbar.update(1)
                if distance[1] == float("inf"):
                    temp = -1
                pre_process[j][i] = temp
        return pre_process

    def get_predecessors(self, distances,start, end):
        index = end
        obj = distances[end]
        predecessors = []

        print(index, "     ", end="")
        if obj[1] == float("inf"):
            print("unreachable")
            return

        predecessor = obj[0]
        temp = []

        while predecessor != start:
            temp.append(predecessor)
            predecessor = distances[predecessor][0]

        for predecessor in reversed(temp):
            predecessors.append(predecessor)
        #predecessors.append(distances[predecessor][0])
        temp = []

        return predecessors, obj[1]

    def reverse(self): 
        reverse = Graph(self.nodes, [])
        for node in self.graph:
            if node is None:
                continue
            for edge in node.edges:
                reverse.add(edge.end, edge.start, edge.weight, self.graph[edge.end].lon, self.graph[edge.end].lat)
        return reverse



    def __repr__(self) -> str:
        return str(self.graph)
