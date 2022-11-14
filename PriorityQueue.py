class PriorityQueue:


    def __init__(self) -> None:
        self.distances = []
        self.length = 0
        self.indexes = []

    def swap(self, i, j):
        self.distances[i], self.distances[j] = self.distances[j], self.distances[i]
        self.indexes[i], self.indexes[j] = self.indexes[j], self.indexes[i]

    @staticmethod
    def left_child_index(i):
        return 2 * i + 1

    @staticmethod
    def right_child_index(i):
        return 2 * i + 2

    @staticmethod
    def parent_index(i):
        return (i - 1) // 2

    def insert(self, index, weight):
        self.distances.append(weight)
        self.indexes.append(index)
        self.length += 1
        self.heapify_up(self.length - 1)

    def change_priority(self, index, weight):
        self.distances[self.indexes[index]] = weight
        self.heapify_up(index)
        return

    def is_in_queue(self, index):
        if index < self.length and self.indexes[index] < self.length:
            print(1)
            return True
        return False

    def peek(self):
        # if self.length == 0:
        #    return None
        self.swap(0, self.length - 1)
        distance = self.distances.pop()
        peek = self.indexes.pop()
        self.length -= 1
        self.heapify_down(0)

        return [peek, distance]

    def heapify_up(self, i):
        while (self.parent_index(i) >= 0) and self.distances[
            self.parent_index(i)
        ] > self.distances[i]:
            self.swap(self.parent_index(i), i)
            i = self.parent_index(i)

    def heapify_down(self, i):
        left_child_index = self.left_child_index(i)
        while left_child_index < self.length:
            smallest_index = left_child_index
            right_child_index = self.right_child_index(i)
            if (
                right_child_index < self.length
                and self.distances[right_child_index] < self.distances[left_child_index]
            ):
                smallest_index = right_child_index
            if self.distances[i] < self.distances[smallest_index]:
                break
            self.swap(i, smallest_index)
            i = smallest_index
            left_child_index = self.left_child_index(i)