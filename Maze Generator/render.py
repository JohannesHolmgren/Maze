""" render.py """

""" 
This file is used to render a MST as a maze.

The MST should be made from a grid (see maze.py) 
and will be drawn as such. Pygame is used for rendering.


Idea:

To iterate through all edges every time to see if it's present would be inefficient.
Instead, create a map/dict with nodes as keys and all connecting edges as a set of values.
Then it's sufficient to iterate through all edges once, add to each node's set.
Complexity is thus O(E)*O(log V) = O(E log V) for E edges and V nodes.
Since the graph is a MST, E = V-1, giving a complexity of O(V log V).

get a MST with size size_x * size_y
Create a map with nodes as keys and outgoing edges as values.

To "remove" a wall is the same as adding it - but drawing a line with the background color
instead of the wall color where it should be. A possible approach would then be:
1. Draw a grid
2. Iterate through all edges. Remove (or add opening, same same) the wall the edge represents.
3. Done

Complexity becomes linear O(E) = O(V-1) for removing all walls that should be removed.

"""
# Standard libraries
import math

# External libraries
import pygame

# Internal libraries
from Graph import Graph, Node
from maze import get_maze
from solver import Solver

# --- Functions for initialize rendering ---
def get_block_size(canvas, size_x, size_y):
    return int(min(canvas.get_width()/size_x, canvas.get_height()/size_y))

def get_dot_size(block_size, fraction):
    return int(block_size/fraction)


# --- Constants for Colors etc. ---
C_BG     = (255, 255, 255)
C_CANVAS = (255, 255, 255)
C_LINE   = (0, 0, 0)
C_START  = (0, 255, 0)
C_GOAL   = (255, 0, 0)
C_PATH   = (0, 0, 255)
C_TEXT   = (0, 0, 0)

# --- Display init ---
win_x, win_y = 850, 600
win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption("Maze Solver")
win.fill(C_BG)

# --- Canvas - How big the maze is allowed to be ---
canvas_x = int(2*win_x/3) + 1   # 2/3 of win
canvas_y = win_y - 20 + 1     # Add one to both to make room for an additional ending line 
offset_x = 10
offset_y = 10
canvas = pygame.Surface((canvas_x, canvas_y))
canvas.fill(C_CANVAS)

# --- Size of maze (To be changed of a possible user) ---
SIZE_X = 30
SIZE_Y = 30

# --- Size of a "block" of the path. Depends on canvas size and size of maze ---
# Should always be quadratic. Calculated using the the maximum size that fits
BLOCK_SIZE = get_block_size(canvas, SIZE_X, SIZE_Y)
DOT_SIZE   = get_dot_size(BLOCK_SIZE, 3)

# --- Graph and Solver initializer ---
g = get_maze(SIZE_X, SIZE_Y)
solver = Solver()
path = []

# --- Text ---
pygame.font.init()
font = pygame.font.SysFont('arial', 15, True)
textes = [
        "D - Start Depth-First-Search",
        "B - Start Breadth-First-Search",
        "R - Shuffle maze",
        "LEFT MOUSE - Move start",
        "RIGHT MOUSE - Move goal"
        ]


# --- Functions ---
def render_text(win, x, y, spacing=10):
    for text in textes:
        text_surface = font.render(text, False, C_TEXT)
        win.blit(text_surface, (x, y))
        y += text_surface.get_height() + spacing

def draw_grid(win, size_x, size_y, block_size):
    """ Used to draw a grid. """
    for x in range(size_x + 1):
        pygame.draw.line(win, C_LINE, (x*block_size, 0), (x*block_size, size_y*block_size), 1)
    for y in range(size_y + 1):
        pygame.draw.line(win, C_LINE, (0, y*block_size), (size_x*block_size, y*block_size), 1)

def remove_wall(win, edge):
    p1 = edge.fro.value
    p2 = edge.to.value
    dir_x = p2[0]-p1[0] # -1 means backwards, 0 same and 1 forward in x-direction
    dir_y = p2[1]-p1[1] # -1 means backwards, 0 same and 1 forward in y-direction
    # Which wall to remove
    if dir_x < 0:
        pygame.draw.line(win, C_CANVAS, (p2[0]*BLOCK_SIZE+BLOCK_SIZE, p2[1]*BLOCK_SIZE+1), (p2[0]*BLOCK_SIZE+BLOCK_SIZE, p2[1]*BLOCK_SIZE+BLOCK_SIZE-1), 1)
        pass # Remove wall to the right of p2
    elif dir_x > 0:
        pygame.draw.line(win, C_CANVAS, (p1[0]*BLOCK_SIZE+BLOCK_SIZE, p1[1]*BLOCK_SIZE+1), (p1[0]*BLOCK_SIZE+BLOCK_SIZE, p1[1]*BLOCK_SIZE+BLOCK_SIZE-1), 1)
        pass # Remove wall to the right of p1
    elif dir_y < 0:
        pygame.draw.line(win, C_CANVAS, (p2[0]*BLOCK_SIZE+1, p2[1]*BLOCK_SIZE+BLOCK_SIZE), (p2[0]*BLOCK_SIZE+BLOCK_SIZE-1, p2[1]*BLOCK_SIZE+BLOCK_SIZE), 1)
        pass # Remove wall below p2
    elif dir_y > 0:
        pygame.draw.line(win, C_CANVAS, (p1[0]*BLOCK_SIZE+1, p1[1]*BLOCK_SIZE+BLOCK_SIZE), (p1[0]*BLOCK_SIZE+BLOCK_SIZE-1, p1[1]*BLOCK_SIZE+BLOCK_SIZE), 1)
        pass # Remove wall below p1
    else:
        raise ValueError("Invalid edge")

def draw_maze(win):
    # win.fill(C_BG)
    canvas.fill(C_CANVAS)
    draw_grid(canvas, SIZE_X, SIZE_Y, BLOCK_SIZE)
    for e in g.edges:
        remove_wall(canvas, e)
    win.blit(canvas, (offset_x, offset_y))

def draw_path_curved(win, path, start, goal):
    curve = lambda p1, p2: (p2[0]-p1[0], p2[1]-p1[1])
    blit_pos = lambda pos: (int(pos[0]*BLOCK_SIZE+BLOCK_SIZE/2), int(pos[1]*BLOCK_SIZE+BLOCK_SIZE/2))
    for index, node in enumerate(path[1:-1], 1):
        dir = curve(path[index-1].value, path[index+1].value)
        if dir[0] == 0:
            # Vertical
            start = (BLOCK_SIZE*node.value[0]+1 + BLOCK_SIZE/2, BLOCK_SIZE*node.value[1]-1)
            end   = (BLOCK_SIZE*node.value[0]+1 + BLOCK_SIZE/2, BLOCK_SIZE*node.value[1]-1 + BLOCK_SIZE)
            pygame.draw.line(win, C_PATH, start, end, width=2)
            # win.blit(vertical, (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]-1))
        elif dir[1] == 0:
            # Horizontal
            start = (BLOCK_SIZE*node.value[0]-1, BLOCK_SIZE*node.value[1]+1 + BLOCK_SIZE/2)
            end = (BLOCK_SIZE*node.value[0]-1 + BLOCK_SIZE, BLOCK_SIZE*node.value[1]+1 + BLOCK_SIZE/2)
            pygame.draw.line(win, C_PATH, start, end, width=2)
            # win.blit(horizontal, (BLOCK_SIZE*node.value[0]-1, BLOCK_SIZE*node.value[1]+1))
        elif dir[0] == 1 and dir[1] == 1:
            # One step down to left
            # Two cases: from vertical or from horizontal
            prev_dir = curve(path[index-1].value, node.value)
            if prev_dir[0] == 1:
                # Horizontal into this block
                mid = (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]+1 + BLOCK_SIZE)
                blit_rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
                blit_rect.center = mid
                start_angle = 0
                stop_angle  = math.pi/2
                pygame.draw.arc(win, C_PATH, blit_rect, start_angle, stop_angle, width=2)
                # win.blit(botleft, (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]+1))
            else:
                # Vertical into this block
                mid = (BLOCK_SIZE*node.value[0]+1 + BLOCK_SIZE, BLOCK_SIZE*node.value[1]+1)
                blit_rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
                blit_rect.center = mid
                start_angle = math.pi
                stop_angle  = 3*math.pi/2
                pygame.draw.arc(win, C_PATH, blit_rect, start_angle, stop_angle, width=2)
                # win.blit(topright, (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]+1))
        elif dir[0] == -1 and dir[1] == 1:
            # Down and to the left
            # Two cases: from vertical or from horizontal
            prev_dir = curve(path[index-1].value, node.value)
            if prev_dir[0] != 0:
                # Horizontal into this block
                mid = (BLOCK_SIZE*node.value[0]+1 + BLOCK_SIZE, BLOCK_SIZE*node.value[1]+1 + BLOCK_SIZE)
                blit_rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
                blit_rect.center = mid
                start_angle = math.pi/2
                stop_angle  = math.pi
                pygame.draw.arc(win, C_PATH, blit_rect, start_angle, stop_angle, width=2)
            else:
                # Vertical into this block
                mid = (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]+1)
                blit_rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
                blit_rect.center = mid
                start_angle = -math.pi/2
                stop_angle  = 0
                pygame.draw.arc(win, C_PATH, blit_rect, start_angle, stop_angle, width=2)
                # win.blit(topleft, (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]+1))
        elif dir[0] == 1 and dir[1] == -1:
            # Up and to the left
            # Two cases: from vertical or from horizontal
            prev_dir = curve(path[index-1].value, node.value)
            if prev_dir[0] != 0:
                # Horizontal into this block
                mid = (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]+1)
                blit_rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
                blit_rect.center = mid
                start_angle = -math.pi/2
                stop_angle  = 0
                pygame.draw.arc(win, C_PATH, blit_rect, start_angle, stop_angle, width=2)
                # win.blit(topleft, (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]+1))
            else:
                # Vertical into this block
                mid = (BLOCK_SIZE*node.value[0]+1 + BLOCK_SIZE, BLOCK_SIZE*node.value[1]+1 + BLOCK_SIZE)
                blit_rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
                blit_rect.center = mid
                start_angle = math.pi/2
                stop_angle  = math.pi
                pygame.draw.arc(win, C_PATH, blit_rect, start_angle, stop_angle, width=2)
                # win.blit(botright, (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]+1))
        else:
            # Up and to the right
            # Two cases: from vertical or from horizontal
            prev_dir = curve(path[index-1].value, node.value)
            if prev_dir[0] != 0:
                # Horizontal into this block
                mid = (BLOCK_SIZE*node.value[0]+1 + BLOCK_SIZE, BLOCK_SIZE*node.value[1]+1)
                blit_rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
                blit_rect.center = mid
                start_angle = math.pi
                stop_angle  = 3*math.pi/2
                pygame.draw.arc(win, C_PATH, blit_rect, start_angle, stop_angle, width=2)
                # win.blit(topright, (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]+1))
            else:
                # Vertical into this block
                mid = (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]+1 + BLOCK_SIZE)
                blit_rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
                blit_rect.center = mid
                start_angle = 0
                stop_angle  = math.pi/2
                pygame.draw.arc(win, C_PATH, blit_rect, start_angle, stop_angle, width=2)
                # win.blit(botleft, (BLOCK_SIZE*node.value[0]+1, BLOCK_SIZE*node.value[1]+1))
    # Draw start and goal
       

def get_coord(pos):
    return (pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE)

  
# --- Main loop ---
start = (0, 0)
goal = (SIZE_X-1, SIZE_Y-1)
redraw = 1
solver_started = False
mode = "DFS"

render_text(win, canvas_x+20, 50)

RUNNING = True
while(RUNNING):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        redraw = 20
    if redraw > 0:
        g = get_maze(SIZE_X, SIZE_Y)
        path = []
        solver_started = False
        draw_maze(win)
        redraw -= 1
    if keys[pygame.K_d]:
        mode = "DFS"
        if not solver_started:
            solver_started = True
            solver.reset()
            solver.set(g, Node(start), Node(goal), mode)
    if keys[pygame.K_b]:
        mode = "BFS"
        if not solver_started:
            solver_started = True
            solver.reset()
            solver.set(g, Node(start), Node(goal), mode)
    # Resizing
    if keys[pygame.K_UP]:
        SIZE_X += 1
        SIZE_Y += 1
        BLOCK_SIZE = get_block_size(canvas, SIZE_X, SIZE_Y)
        DOT_SIZE = get_dot_size(BLOCK_SIZE, 3)
        g = get_maze(SIZE_X, SIZE_Y)
        draw_maze(win)
    # Reucing size gives some bugs that must be fixed before impl.
    # Mouse input
    if pygame.mouse.get_pressed()[0]:
        if not solver_started:
            pos = pygame.mouse.get_pos()
            coord = get_coord(pos)
            if 0 <= coord[0] < SIZE_X and 0 <= coord[1] < SIZE_Y: 
                start = coord
        elif solver.finished:
            pos = pygame.mouse.get_pos()
            coord = get_coord(pos)
            if 0 <= coord[0] < SIZE_X and 0 <= coord[1] < SIZE_Y: 
                start = coord
            # Reset and create a new path
            solver.reset()
            solver.set(g, Node(start), Node(goal), mode)
            path = solver.get_all()
    if pygame.mouse.get_pressed()[2]:
        if not solver_started:
            pos = pygame.mouse.get_pos()
            coord = get_coord(pos)
            if 0 <= coord[0] < SIZE_X and 0 <= coord[1] < SIZE_Y: 
                goal = coord
        elif solver.finished:
            pos = pygame.mouse.get_pos()
            coord = get_coord(pos)
            if 0 <= coord[0] < SIZE_X and 0 <= coord[1] < SIZE_Y: 
                goal = coord
            # Reset and create a new path
            solver.reset()
            solver.set(g, Node(start), Node(goal), mode)
            path = solver.get_all()

    if solver_started:
        path = solver.next()
        
    draw_maze(win)
    pygame.draw.circle(canvas, C_START, (int(start[0]*BLOCK_SIZE+BLOCK_SIZE/2), int(start[1]*BLOCK_SIZE+BLOCK_SIZE/2)), DOT_SIZE)
    pygame.draw.circle(canvas, C_GOAL, (int(goal[0]*BLOCK_SIZE+BLOCK_SIZE/2), int(goal[1]*BLOCK_SIZE+BLOCK_SIZE/2)), DOT_SIZE)
    draw_path_curved(canvas, path, start, goal)
    win.blit(canvas, (offset_x, offset_y))

    
    pygame.display.update()
    pygame.time.Clock().tick(60)
    
    