# Maze
This program generates, solves and visualizes a maze.

=== Maze generator ===
The maze is generated using a Minimal Spanning Tree (MST) with random edge-costs. A maze can be seen as a grid where it's possible to go to some neighbours and not to others. Using this way of seeing it, the grid-positions is converted to nodes in a graph, and the neighbour-neighbour relation is an edge. The edges are then given a random cost. An algorithm called Prim's algorithm is then run to create an MST. This ensures that all nodes have a path to all other nodes in the maze.

This article was used for reference: \href(https://www.baeldung.com/cs/maze-generation)

