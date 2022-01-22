""" maze.py """

"""
This file implements functions to create a maze.

The method used is to create generate a maze using a 
Minimal Spanning Tree with random edge cost. 

This article was used for reference: https://www.baeldung.com/cs/maze-generation

Create a grid - N by M size
Transform into a graph

"""
from random import random
from queue import PriorityQueue
from Graph import Graph, Node, Edge

def grid_to_graph(grid):
    """ Takes a grid and creates a graph with positions in the grid as 
        nodes and neighbours as edges and gives a random cost to every edge """
    N = len(grid)
    M = len(grid[0])
    g = Graph()
    for n in range(N):
        for m in range(M):
            node = Node((n, m))
            g.add_node(node)
            if not n == N-1:
                to = Node((n+1, m))
                cost = random()
                edge = Edge(node, to, cost)
                g.add_node(to)
                g.add_edge(edge)
            if not m == M-1:
                to = Node((n, m+1))
                cost = random()
                edge = Edge(node, to, cost)
                g.add_node(to)
                g.add_edge(edge)
    return g

def get_MST(graph: Graph) -> Graph:
    """ Uses Prim's algorithm to create a minimum spanning tree. """
    # Sort all edges
    # Choose a start node
    # Add all outgoing edges to a priority queue
    # Remove the first edge. If it has more than one endpoint in the graph
    # (both nodes already added) then skip it
    # Otherwise add the node to the graph and all outgoing edges with one endpoint
    # in the graph.

    mst = Graph()
    pqueue = PriorityQueue()

    # Set a start node (ugly but there is no simple way to get an item from a set without removing it)
    start = next(iter(graph.nodes))
    mst.add_node(start)
    # Get outgoing edges
    outgoing = graph.get_edges2(start)
    # Add to PQ
    for e in outgoing:
        pqueue.put(e)
    
    # A MST have N-1 edges where N is the number of nodes in the tree
    while(len(mst.edges) < len(graph.nodes)-1):
        min_edge = pqueue.get()
        # Test if it has more than one endpoint in mst
        if min_edge.fro in mst.nodes and min_edge.to in mst.nodes:
            continue
        # Add the node which is not in the mst yet
        new_node = min_edge.fro if not min_edge.fro in mst.nodes else min_edge.to
        mst.add_node(new_node)
        # The edge is part of the MST of the graph
        mst.add_edge(min_edge)
        # Add all outgoing edges to the queue
        outgoing = graph.get_edges2(new_node)
        for e in outgoing:
            pqueue.put(e)
    return mst

def get_maze(width, height):
    """ Combines functions grid_to_graph and get_mst to a nice, 
        easy to read function for creating MST to be used as mazes. """
    # What type the elements have is arbitrary, only indexes are of interest
    grid = [[None]*height]*width
    return get_MST(grid_to_graph(grid))
