""" solver.py """

"""
This file contains function for solving a maze 
by finding the shortest path from one node (or position) to another.

"""


from ast import Str
from collections import deque

class Entry:
    """ Wrapper class used to easily find the way back when goal is reached """

    def __init__(self, node, backpointer):
        self.node = node
        self.backpointer = backpointer


class Solver:

    def __init__(self):
        self.collection = deque()
        self.visited = set()
        self.graph = None
        self.start = None
        self.goal = None
        self.path = []
        self.finished = False
        self.mode = None

    def set_mode(self, mode: Str):
        if not mode in ("BFS", "DFS"):
            raise ValueError("The mode must either be BFS or DFS")
        self.mode = mode

    def set(self, graph, start, goal, mode):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.collection.append(Entry(start, None))
        self.set_mode(mode)

    def reset(self):
        self.collection.clear()
        self.visited.clear()
        self.path = []
        self.finished = False


    def BFS(self, graph, start, goal):

        
        # Create a collection
        # Create a set with visited nodes - combined with what node it came from
        # Add start node to the collection
        # While collection is not empty:
        #   Decollection a node
        #   If goal: found it. Quit loop
        #   For all its edges:
        #       If not going to a visited node:
        #           Add node to collection together with what it came from
        #   Check what previous node this node came from
        #   Add to visited.
        self.mode = "BFS"
        self.graph = graph
        self.start = start
        self.goal = goal
        self.path = []
        self.finished = False
        self.collection.clear()
        self.visited.clear()
        self.collection.append(Entry(start, None))

    def DFS(self, graph, start, goal):
        self.mode = "DFS"
        self.graph = graph
        self.start = start
        self.goal = goal
        self.path = []
        self.finished = False
        self.collection.clear()
        self.visited.clear()
        self.collection.append(Entry(start, None))


    def next(self):
        if self.finished:
            return self.path
        if self.mode == "BFS":
            entry = self.collection.popleft()
        elif self.mode == "DFS":
            entry = self.collection.pop()
        if entry.node == self.goal:
            self.finished = True
            return self.get_path(entry)
        edges = self.graph.get_edges2(entry.node)
        for edge in edges:
            # Get the "other" node
            to = edge.to if not edge.to == entry.node else edge.fro
            if not to in self.visited:
                self.collection.append(Entry(to, entry))
        self.visited.add(entry.node)
        return self.get_path(entry)

    def get_all(self):
        while not self.finished:
            self.path = self.next()
        return self.path


    def get_path(self, entry):
        path = []
        while(entry is not None):
            path.append(entry.node)
            entry = entry.backpointer
        path.reverse()
        self.path = path
        return path


