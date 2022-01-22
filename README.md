# Maze
This program generates, solves and visualizes a maze. Knowledge in Algorithms and Data structures was used to optimize the program in order to handle larger mazes.

=== Maze generator ===
The maze.py handles the generating of mazes. The maze is generated using a Minimal Spanning Tree (MST) with random edge-costs. A maze can be seen as a grid where it's possible to go to some neighbours and not to others. Using this way of seeing it, the grid-positions is converted to nodes in a graph, and the neighbour-neighbour relation is an edge. The edges are then given a random cost. An algorithm called Prim's algorithm is then run to create an MST. This ensures that all nodes have a path to all other nodes in the maze.

This article was used for reference: https://www.baeldung.com/cs/maze-generation

=== Maze Solver ===
The solver.py contains the class Solver which takes care of the solving of the maze. It supports two different algorithms: breadth-first-search (BFS) and depth-first-search (DFS). It has two different ways of getting the path: next() - which gives the path to the next node working algorithm visits, and get_all() - which gives the entire path from start to goal. The first method is used to visualize how the algorithm proceeds through the maze, while the other is practical to use when the user moves around the start and goal after the algoritm has finished.

=== Maze Render ===
The render.py file handles the rendering as well as the UI. It implements user-input using the mouse and buttons to switch between different solving algorithms, regenerating of the maze as well as moving the start and goal around.
