from dataclasses import dataclass
import tqdm
from PriorityQueue import PriorityQueue
from timeit import default_timer as timer


@dataclass
class Edge:
    start: int
    end: int
    weight: int


@dataclass
class Node:
    value: int
    edges: list[Edge]
    lon: float = None
    lat: float = None
    estimated: int = None

    def append_edge(self, end: int, weight: int) -> None:
        self.edges.append(Edge(self.value, end, weight))


class Graph:
    nodes: int
    edges: list[Edge]
    graph: list[Node]
    estimated: int = None

    def __init__(self, nodes: int, edges: list[Edge]) -> None:
        self.nodes = nodes
        self.edges = edges
        self.graph = [None] * self.nodes

    def add(
        self, start: int, end: int, weight: int, lon: float = None, lat: float = None
    ) -> None:
        if self.graph[start] is not None:
            self.graph[start].append_edge(end, weight)
            return
        self.graph[start] = Node(start, [Edge(start, end, weight)], lon, lat)

    def dijikstras(self, start: int, stop: int = None, only_distances: bool = False):
        distances = [[None, float("inf")]] * self.nodes
        distances[start] = ["start", 0]
        queue = PriorityQueue()
        queue.insert(self.graph[start].value, 0)
        nodes = 0

        visited = [False] * self.nodes
        # pbar = tqdm.tqdm(total=self.nodes)
        # print("Finding paths...")
        if not only_distances:
            print("Finding path with dijikstra...")
            start = timer()
        while queue.length != 0:
            nodes += 1
            index, distance = queue.peek()
            current_node = self.graph[index]

            if stop is not None and index == stop:
                break

            if current_node is None:
                continue
            if visited[index]:
                continue
            # pbar.update(1)
            visited[index] = True
            distances[current_node.value][1] = distance

            for edge in current_node.edges:
                if visited[edge.end]:
                    continue
                new_weight = distance + edge.weight
                if new_weight < distances[edge.end][1]:
                    queue.insert(edge.end, new_weight)
                    distances[edge.end] = [edge.start, new_weight]
        end = timer() - start
        if not only_distances:
            print(f"done. ({end})")
            print(f"processed {nodes} nodes")

        if stop is None:
            return distances
        if only_distances:
            return distances[stop][1]
        return self.get_predecessors(distances, stop)

    def alt(
        self,
        start: int,
        stop: int,
        preprocess_from: list[list[int]],
        preprocess_to: list[list[int]],
    ):
        distances = [[None, float("inf")]] * self.nodes
        distances[start] = ["start", 0]
        queue = PriorityQueue()
        estimated_end = self.estimate_distance(preprocess_from, preprocess_to, start, stop)
        queue.insert(self.graph[start].value, estimated_end)
        nodes = 0
        visited = [False] * self.nodes
        # pbar = tqdm.tqdm(total=self.nodes)
        # print("Finding paths...")
        print("Finding path with alt...")
        start = timer()
        while queue.length != 0:
            index, distance = queue.peek()
            current_node = self.graph[index]
            nodes += 1

            if stop is not None and index == stop:
                break
            if current_node is None:
                continue
            if visited[index]:
                continue

            # pbar.update(1)
            visited[index] = True
            distances[current_node.value][1] = distance

            for edge in current_node.edges:
                if visited[edge.end]:
                    continue
                new_weight = distance + edge.weight
                if new_weight < distances[edge.end][1]:
                    estimated_end = self.estimate_distance(
                        preprocess_from, preprocess_to, index, edge.end
                    )

                    queue.insert(edge.end, new_weight + estimated_end)
                    distances[edge.end] = [edge.start, new_weight]
        end = timer() - start
        print(f"done. ({end})")
        print(f"processed {nodes} nodes")

        if stop is None:
            return distances
        return self.get_predecessors(distances, stop)

    def estimate_distance(
        self,
        preprocess_from: list[list[int]],
        preprocess_to: list[list[int]],
        start: int,
        stop: int,
    ):
        max_difference = 0
        for i in range(len(preprocess_from[0])):
            to_node = preprocess_to[start][i] - preprocess_to[stop][i]
            from_landmark = preprocess_from[stop][i] - preprocess_from[start][i]

            if to_node > max_difference:
                max_difference = to_node

            if from_landmark > max_difference:
                max_difference = from_landmark

        return max_difference

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

    def get_predecessors(self, distances, end):
        obj = distances[end]
        predecessors = []

        if obj[1] == float("inf"):
            return

        predecessor = obj[0]
        temp = []

        while predecessor != "start":
            temp.append(predecessor)
            predecessor = distances[predecessor][0]

        for predecessor in reversed(temp):
            predecessors.append(self.graph[predecessor])
        predecessors.append(self.graph[end])
        temp = []

        return predecessors, obj[1]

    def reverse(self):
        reverse = Graph(self.nodes, [])
        for node in self.graph:
            if node is None:
                continue
            for edge in node.edges:
                reverse.add(edge.end, edge.start, edge.weight, None, None)
        return reverse

    def __repr__(self) -> str:
        return str(self.graph)
