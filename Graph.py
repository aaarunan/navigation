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

    def __init__(self, nodes: int) -> None:
        self.nodes = nodes
        self.graph = [Node(i, []) for i in range(nodes)]

    def add_connection(self, start: int, end: int, weight: int) -> None:
        self.graph[start].append_edge(end, weight)

    def reverse(self):
        reverse = Graph(self.nodes)
        for node in self.graph:
            for edge in node.edges:
                reverse.add_connection(edge.end, edge.start, edge.weight)
        return reverse

    def dijikstras(self, start: int, stop: int):
        distances = {}
        distances[start] = [-1, 0]
        queue = PriorityQueue()
        queue.put((0, self.graph[start].value))
        visited = set()
        nodes = 0

        start_timer = timer()
        while not queue.empty():
            nodes += 1
            distance, index = queue.get()

            if index in visited:
                continue
            if index == stop:
                time = timer() - start_timer
                return (
                    self.predecessors(distances, stop),
                    time,
                    nodes,
                    distances[stop][1],
                )
            current_node = self.graph[index]
            visited.add(index)
            distances[index][1] = distance

            for edge in current_node.edges:
                if edge.end in visited:
                    continue
                if edge.end not in distances:
                    distances[edge.end] = [None, float("inf")]
                new_weight = distance + edge.weight
                if new_weight < distances[edge.end][1]:
                    queue.put((new_weight, edge.end))
                    distances[edge.end] = [index , new_weight]
        return False

    def dijikstra_all(
        self, start: int, typ: int, silent: bool = False
    ) -> tuple[list[list[int]], PriorityQueue]:
        distances = {}
        distances[start] = [-1, 0]
        queue = PriorityQueue()
        queue.put((0, self.graph[start].value))
        visited = set()
        targets = PriorityQueue()
        nodes = 0

        if not silent:
            pbar = tqdm(total=self.nodes)
            print("Finding path with dijikstra...")
        while not queue.empty():
            nodes += 1
            distance, index = queue.get()
            current_node = self.graph[index]
            if not silent:
                pbar.update(1)

            if index in visited:
                continue
            if current_node.type is not None and current_node.type & typ == typ:
                targets.put((distance, index))
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
                    distances[edge.end] = [index, new_weight]
        return distances, targets

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
        p_from: list[list[int]],
        p_to: list[list[int]],
    ):
        estimated_end = self.estimeate_end(p_from, p_to, start, stop)
        queue = PriorityQueue()
        queue.put((estimated_end, self.graph[start].value))
        distances = {}
        distances[start] = [-1, 0, estimated_end]
        visited = set()
        nodes = 0

        start_time = timer()
        while not queue.empty():
            nodes += 1
            _, index = queue.get()

            if index in visited:
                continue
            if index == stop:
                time = timer() - start_time
                return (
                    self.predecessors(distances, stop),
                    time,
                    nodes,
                    distances[stop][1],
                )
            current_node = self.graph[index]

            visited.add(index)

            for edge in current_node.edges:
                if edge.end in visited:
                    continue
                new_weight = distances[index][1] + edge.weight
                if edge.end not in distances:
                    distances[edge.end] = [None, float("inf"), None]
                if new_weight < distances[edge.end][1]:
                    estimated_end = distances[edge.end][2]
                    if estimated_end is None:
                        estimated_end = self.estimeate_end(p_from, p_to, edge.end, stop)
                    queue.put((new_weight + estimated_end, edge.end))
                    distances[edge.end] = [
                        index,
                        new_weight,
                        estimated_end,
                    ]

        return False

    def estimeate_end(
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

    def predecessors(self, distances, stop):
        current = distances[stop]
        predecessors = []

        if current[1] == float("inf"):
            return

        predecessor = current[0]
        temp = []

        # kan fjernes
        while predecessor != -1:
            temp.append(predecessor)
            predecessor = distances[predecessor][0]

        for predecessor in reversed(temp):
            predecessors.append(self.graph[predecessor])
        predecessors.append(self.graph[stop])
        temp = []

        return predecessors, current[1]

    def __repr__(self) -> str:
        return str(self.graph)
