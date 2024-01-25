import random, pygame, os
import time as t
from pygame import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

global SCREEN

WIDTH = 50
HEIGHT = WIDTH
ITERATOR = (-1, 0, 1)

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
YELLOW = (255, 233, 0)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = WINDOW_WIDTH

BLOCK_SIZE = WINDOW_WIDTH // WIDTH

display.set_caption('Game Of Life')

grid = [[False] * HEIGHT for _ in range(WIDTH)]


def random_grid():
    for i in range(WIDTH):
        for j in range(HEIGHT):
            grid[i][j] = random.random() < .5

def clear_grid():
    for i in range(WIDTH):
        for j in range(HEIGHT):
            grid[i][j] = False

def neighbours(pos_x, pos_y):
    nb = 0

    for x in ITERATOR:
        for y in ITERATOR:
            if x == 0 and y == 0:
                continue
            nb += int(grid[(pos_x + x) % WIDTH][(pos_y + y) % HEIGHT])

    return nb


def next_gen():
    temp = [[False] * HEIGHT for _ in range(WIDTH)]

    for x in range(WIDTH):
        for y in range(HEIGHT):
            nb = neighbours(x, y)
            temp[x][y] = (grid[x][y] and nb >= 2 and nb <= 3) or ((not grid[x][y]) and nb == 3)

    return temp


def draw_frame():
    drawGrid()
    display.update()


def drawGrid():
    SCREEN.fill(BLACK)
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = Rect(x+1, y+1, BLOCK_SIZE-2, BLOCK_SIZE-2)
            if grid[x // BLOCK_SIZE][y // BLOCK_SIZE]:
                draw.rect(SCREEN, YELLOW, rect)


random_grid()

SCREEN = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
SCREEN.fill(BLACK)

delay = 0.0

running = True
paused = False
drawing = False
erasing = False

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                paused = not paused
            if event.key == K_RIGHT:
                for num, row in enumerate(next_gen()):
                    grid[num] = row.copy()
            if event.key == K_UP:
                delay += .01
            if event.key == K_DOWN and delay > 0.01:
                delay -= .01
            if event.key == K_LEFT:
                clear_grid()
            if event.key == K_r:
                random_grid()

        elif event.type == MOUSEBUTTONDOWN:
            drawing = True
            start_x, start_y = mouse.get_pos()
            erasing = grid[start_x // BLOCK_SIZE][start_y // BLOCK_SIZE]
        elif event.type == MOUSEBUTTONUP:
            drawing = False

    if drawing:
        x, y = mouse.get_pos()
        x //= BLOCK_SIZE
        y //= BLOCK_SIZE
        if grid[x][y] == erasing:
            grid[x][y] = not grid[x][y]
            draw_frame()

    draw_frame()

    if not paused:
        for num, row in enumerate(next_gen()):
            grid[num] = row.copy()
        draw_frame()

    t.sleep(delay)

pygame.quit()
