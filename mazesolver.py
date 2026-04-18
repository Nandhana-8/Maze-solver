import pygame
import heapq
import sys
import time

pygame.init()

# Window
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver - A* Search")

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
GRAY = (200,200,200)

# Maze Grid
grid = [
    [0,0,0,1,0,0,0,0,0,0],
    [1,1,0,1,0,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,1,0,0,0,1,0],
    [1,1,1,0,1,1,1,0,1,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,0,0,0,1,0]
]

start = (0,0)
goal = (9,9)

visited = []
path = []

# Draw Grid
def draw():
    screen.fill(WHITE)

    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE

            if grid[i][j] == 1:
                color = BLACK
            if (i,j) in visited:
                color = GRAY
            if (i,j) in path:
                color = YELLOW
            if (i,j) == start:
                color = GREEN
            if (i,j) == goal:
                color = RED

            pygame.draw.rect(screen, color, (j*CELL, i*CELL, CELL, CELL))
            pygame.draw.rect(screen, BLUE, (j*CELL, i*CELL, CELL, CELL), 1)

    pygame.display.update()

# Heuristic
def h(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# A* Search
def astar():
    pq = []
    heapq.heappush(pq, (0,start))
    came = {}
    cost = {start:0}

    while pq:
        current = heapq.heappop(pq)[1]

        if current not in visited:
            visited.append(current)

        draw()
        time.sleep(0.15)

        if current == goal:
            break

        for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = current[0]+dx, current[1]+dy

            if 0 <= nx < ROWS and 0 <= ny < COLS:
                if grid[nx][ny] == 0:
                    new_cost = cost[current] + 1

                    if (nx,ny) not in cost or new_cost < cost[(nx,ny)]:
                        cost[(nx,ny)] = new_cost
                        priority = new_cost + h(goal,(nx,ny))
                        heapq.heappush(pq,(priority,(nx,ny)))
                        came[(nx,ny)] = current

    # Rebuild shortest path
    node = goal
    while node != start:
        path.append(node)
        draw()
        time.sleep(0.2)
        node = came[node]

    path.append(start)

# Run algorithm
astar()

# Main loop
while True:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()