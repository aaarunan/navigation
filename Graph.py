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

    def reverse(self):
        reverse = Graph(self.nodes, [])
        for node in self.graph:
            if node is None:
                continue
            for edge in node.edges:
                reverse.add(edge.end, edge.start, edge.weight, None, None)
        return reverse

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
        return self.get_predecessors(distances, start, stop)

    def alt(
        self,
        start: int,
        stop: int,
        preprocess_from: list[list[int]],
        preprocess_to: list[list[int]],
        silent: bool = False,
    ):
        queue = PriorityQueue()
        estimated_end = self.estimate_distance(
            preprocess_from, preprocess_to, start, stop
        )
        queue.insert(self.graph[start].value, estimated_end)
        distances = {}
        distances[start] = ["start", 0, estimated_end]
        nodes = 0
        visited = set()
        if not silent:
            pbar = tqdm.tqdm(total=self.nodes)
            print("Finding path with alt...")
        start_time = timer()
        while queue.length != 0:
            index, _ = queue.peek()
            current_node = self.graph[index]
            nodes += 1

            if current_node is None:
                continue
            if index in visited:
                continue
            if index == stop:
                if not silent:
                    end = timer() - start_time
                    print(f"done. ({end})")
                    print(f"processed {nodes} nodes")
                return self.get_predecessors(distances, start, stop)

            if not silent:
                pbar.update(1)
                visited.add(index)

            for edge in current_node.edges:
                if edge.end in visited:
                    continue
                new_weight = distances[current_node.value][1] + edge.weight
                if edge.end not in distances:
                    distances[edge.end] = [None, float("inf"), None]
                if new_weight < distances[edge.end][1]:
                    estimated_end = distances[edge.end][2]
                    if estimated_end is None:
                        estimated_end = self.estimate_distance(
                            preprocess_from, preprocess_to, edge.end, stop
                        )
                    queue.insert(edge.end, new_weight + estimated_end)
                    distances[edge.end] = [
                        edge.start,
                        new_weight,
                        estimated_end,
                    ]

        return False

    def estimate_distance(
        self,
        to_nodes: list[list[int]],
        to_landmarks: list[list[int]],
        start: int,
        stop: int,
    ):
        max_difference = 0
        for i in range(len(to_nodes[0])):
            to_node = to_landmarks[start][i] - to_landmarks[stop][i]
            from_landmark = to_nodes[stop][i] - to_nodes[start][i]

            if to_node > max_difference:
                max_difference = to_node

            if from_landmark > max_difference:
                max_difference = from_landmark

        return max_difference

    def dijkstra_from_nodes(self, nodes) -> list[list[int]]:
        pre_process = [([None] * len(nodes))[:] for _ in range(self.nodes)]

        pbar = tqdm.tqdm(total=self.nodes * len(nodes))

        for i, landmark in enumerate(nodes):
            distances = self.dijikstras(landmark, only_distances=True)
            for j, distance in enumerate(distances):
                temp = distance[1]
                pbar.update(1)
                if distance[1] == float("inf"):
                    temp = -1
                pre_process[j][i] = temp
        return pre_process

    def get_predecessors(self, distances, start, stop):
        obj = distances[stop]
        print(start)
        predecessors = [self.graph[start]]

        if obj[1] == float("inf"):
            return

        predecessor = obj[0]
        temp = []

        while predecessor != "start":
            temp.append(predecessor)
            predecessor = distances[predecessor][0]

        for predecessor in reversed(temp):
            predecessors.append(self.graph[predecessor])
        predecessors.append(self.graph[stop])
        temp = []

        return predecessors, obj[1]

    def __repr__(self) -> str:
        return str(self.graph)
