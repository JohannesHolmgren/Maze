""" Graph.py """
"""
A class representing a graph with a set of nodes and a set of undirected edges.


Class variables:

nodes - a set containing all nodes
edges = A set containing edges

Class methods:

getEdges(from) - Gives all edges going out from a node (linear complexity)
removeEdge(from, to) - Deletes an edge from the graph
removeNode(node) - Deletes a node, including all its edges, from the graph
addEdge(from, to) - Adds an edge between from and to to the graph (if not already present)
addNode(from, to) - Adds a node to the graph (if not already present)

Internal classes:

Node:

Class variables:

value - its value


Class methods:

comparators, e.g.
__eq__
__gt__
etc...


Edge:

Class variables:
Node from
Node to
(double cost)


"""

from typing import List


class Node:

    def __init__(self, value):
        self.value = value

    def __eq__(self, __o: object) -> bool:
        return self.value == __o

    def __gt__(self, __o: object) -> bool:
        return self.value > __o

    def __lt__(self, __o: object) -> bool:
        return self.value < __o

    def __ge__(self, __o: object) -> bool:
        return self.value >= __o

    def __le__(self, __o: object) -> bool:
        return self.value <= __o

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return str(self.value)

class Edge:

    def __init__(self, fro: Node, to: Node, cost: float=0):
        self.fro = fro
        self.to = to
        self.cost = cost

    def __eq__(self, __o: object) -> bool:
        return self.fro == __o.fro and self.to == __o.to

    def __lt__(self, __o: object) -> bool:
        return self.cost < __o.cost
        
    def __gt__(self, __o: object) -> bool:
        return self.cost > __o.cost

    def __hash__(self) -> int:
        return hash(self.fro) * 13 + hash(self.to) * 17

    def __str__(self) -> str:
        return f"(from: {self.fro}, to: {self.to}, cost: {self.cost})"


class Graph:

    def __init__(self, nodes:list=[], edges:list=[]):
        self.nodes = set()
        self.edges = set()
        self.outgoing = dict()
        for node in nodes:
            self.add_node(node)
            self.outgoing[node] = []
        for edge in edges:
            self.add_edge(edge)
            # Add to dict
            self.outgoing[edge.fro].append(edge)
            self.outgoing[edge.to].append(edge)

    def add_node(self, node: Node):
        self.nodes.add(node)
        if not node in self.outgoing:
            self.outgoing[node] = []

    def remove_node(self, node):
        if not node in self.nodes:
            raise KeyError("The node does not exist")
        outgoing = self.get_edges2(node)
        for e in outgoing:
            self.remove_edge(e)
        self.nodes.remove(node)
        del self.outgoing[node]

    def add_edge(self, e:Edge):
        if not (e.fro in self.nodes and e.to in self.nodes):
            raise KeyError("One or both of the nodes does not exist")
        self.edges.add(e)
        # Add to dict
        self.outgoing[e.fro].append(e)
        self.outgoing[e.to].append(e)

    def remove_edge(self, e:Edge):
        if not e in self.edges:
            raise KeyError("The edge does not exist")
        self.edges.remove(e)
        # Remove from dict
        self.outgoing[e.fro].remove(e)
        self.outgoing[e.to].remove(e)

    def get_edges(self, fro:Node) -> set:
        """ DEPRECATED. Use Node.get_edges() instead since that is faster.
            Returns all edges going to or from a node.
            Complexity: O(E) where E is the number of edges in the graph. """
        edges = set()
        if not fro in self.nodes:
            raise KeyError("The node does not exist")
        for e in self.edges:
            if e.fro == fro or e.to == fro:
                edges.add(e)
        return edges

    def get_edges2(self, fro: Node) -> set:
        return set(self.outgoing[fro])




    