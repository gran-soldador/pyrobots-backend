import heapq


class Heap(list):
    """heapq Wrapper
    """
    def push_back(self, item):
        heapq.heappush(self, item)

    def pop_front(self):
        return heapq.heappop(self)

    def front(self):
        return self[0]
