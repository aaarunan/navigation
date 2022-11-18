from dataclasses import dataclass
from tqdm import tqdm
from timeit import default_timer as timer
from queue import PriorityQueue as PriorityQueue


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
    type: int = None

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
        self, start: int, end: int, weight: int, lon: float = None, lat: float = None, type:int = None
    ) -> None:
        if self.graph[start] is not None:
            self.graph[start].append_edge(end, weight)
            return
        self.graph[start] = Node(start, [Edge(start, end, weight)], lon, lat, type)

    def reverse(self):
        reverse = Graph(self.nodes, [])
        for node in self.graph:
            if node is None:
                continue
            for edge in node.edges:
                reverse.add(edge.end, edge.start, edge.weight)
        return reverse

    def dijikstras(self, start: int, stop: int = None, silent: bool = False):
        distances = {}
        distances[start] = ["start", 0]
        queue = PriorityQueue()
        queue.put((0, self.graph[start].value))
        visited = set()
        nodes = 0

        if not silent:
            print("Finding path with dijikstra...")
            start_timer = timer()
        while not queue.empty():
            nodes += 1
            distance, index = queue.get()
            current_node = self.graph[index]

            if current_node is None:
                continue
            if index in visited:
                continue
            if index == stop:
                pred = self.get_predecessors(distances, start, stop)
                if not silent:
                    end = timer() - start_timer
                    print(f"done. ({end})")
                    print(f"processed {nodes} nodes")
                    print(f"distance       {distances[stop][1]/100/60/60} timer")
                    print(f"Nodes in path: {len(pred[0])}")
                return pred
            visited.add(index)
            distances[current_node.value][1] = distance

            for edge in current_node.edges:
                if edge.end in visited:
                    continue
                if edge.end not in distances:
                    distances[edge.end] = [None, float("inf")]
                new_weight = distance + edge.weight
                if new_weight < distances[edge.end][1]:
                    queue.put((new_weight, edge.end))
                    distances[edge.end] = [edge.start, new_weight]
        return False

    def d(self, node: int, typ: int , silent: bool = False):
        distances = [[0, float("inf")][:] for _ in range(self.nodes)]
        distances[node] = ["start", 0]
        queue = PriorityQueue()
        queue.put((0, self.graph[node].value))
        nodes = 0
        visited = [False] * self.nodes

        if not silent:
            pbar = tqdm(total=self.nodes)
            print("Finding path with dijikstra...")
        while not queue.empty():
            nodes += 1
            distance, index = queue.get()
            current_node = self.graph[index]

            if not silent:
                pbar.update(1)
            if current_node is None:
                continue
            if visited[index]:
                continue
            if current_node.type is not None and current_node.type & typ == typ:
                if not silent:
                    print(f"processed {nodes} nodes")
                yield self.get_predecessors(distances, node, index)

            visited[index] = True
            distances[current_node.value][1] = distance

            for edge in current_node.edges:
                if visited[edge.end]:
                    continue
                new_weight = distance + edge.weight
                if new_weight < distances[edge.end][1]:
                    queue.put((new_weight, edge.end))
                    distances[edge.end] = [index, new_weight]

        return False

    def dijikstra_from_node(self, node: int, silent: bool = False) -> list[list[int]]:
        distances = [float("inf")] * self.nodes
        distances[node] = 0
        queue = PriorityQueue()
        queue.put((0, self.graph[node].value))
        nodes = 0
        visited = [False] * self.nodes

        if not silent:
            pbar = tqdm(total=self.nodes)
            print("Finding path with dijikstra...")
        while not queue.empty():
            nodes += 1
            distance, index = queue.get()
            current_node = self.graph[index]

            if not silent:
                pbar.update(1)
            if current_node is None:
                continue
            if visited[index]:
                continue

            visited[index] = True
            distances[current_node.value] = distance

            for edge in current_node.edges:
                if visited[edge.end]:
                    continue
                new_weight = distance + edge.weight
                if new_weight < distances[edge.end]:
                    queue.put((new_weight, edge.end))
                    distances[edge.end] = new_weight

        return distances

    def alt(
        self,
        start: int,
        stop: int,
        preprocess_from: list[list[int]],
        preprocess_to: list[list[int]],
        silent: bool = False,
    ):
        estimated_end = self.estimate_distance(
            preprocess_from, preprocess_to, start, stop
        )
        queue = PriorityQueue()
        queue.put((estimated_end, self.graph[start].value))
        distances = {}
        distances[start] = ["start", 0, estimated_end]
        visited = set()
        nodes = 0

        if not silent:
            print("Finding path with alt...")
            start_time = timer()
        while not queue.empty():
            _, index = queue.get()
            current_node = self.graph[index]
            nodes += 1

            if current_node is None:
                continue
            if index in visited:
                continue
            if index == stop:
                pred = self.get_predecessors(distances, start, stop)
                if not silent:
                    end = timer() - start_time
                    print(f"done. ({end})")
                    print(f"processed      {nodes} nodes")
                    print(f"distance       {distances[stop][1]/100/60/60} timer")
                    print(f"Nodes in path: {len(pred[0])}")
                return pred

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
                    queue.put((new_weight + estimated_end, edge.end))
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

    def get_predecessors(self, distances, start, stop):
        current = distances[stop]
        predecessors = []

        if current[1] == float("inf"):
            return

        predecessor = current[0]
        temp = []

        while predecessor != "start":
            temp.append(predecessor)
            predecessor = distances[predecessor][0]

        for predecessor in reversed(temp):
            predecessors.append(self.graph[predecessor])
        predecessors.append(self.graph[stop])
        temp = []

        return predecessors, current[1]

    def __repr__(self) -> str:
        return str(self.graph)
