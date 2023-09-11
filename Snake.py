import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

WHITE = (255, 255, 255)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 80 # Can modify later

def update_ui(self):
    self.display.fill(BLACK)
    for pt in self.snake:
        pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x*BLOCK_SIZE, pt.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x*BLOCK_SIZE+4, pt.y*BLOCK_SIZE+4, 12, 12))

    pygame.draw.rect(self.display, WHITE, pygame.Rect(self.food.x*BLOCK_SIZE, self.food.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    text = font.render("Score: " + str(self.score), True, WHITE)
    self.display.blit(text, [0, 0])
    self.display.flip()

def __init__(self, w=640, h=480): # Dimensions
    self.w = w
    self.h = h
    self.display = pygame.display.set_mode((self.w, self.h))
    pygame.display.set_caption('Snake')
    self.clock = pygame.time.Clock()
    self.reset()

def reset(self): # Game state
    self.direction = Direction.RIGHT
    self.head = Point(self.w/2/BLOCK_SIZE, self.h/2/BLOCK_SIZE)
    self.snake = [self.head, Point(self.head.x-1, self.head.y), Point(self.head.x-2, self.head.y)]
    self.score = 0
    self.food = None
    self._place_food()
    self.frame_iteration = 0

def generate_food(self):
    x = random.randint(0, (self.w-BLOCK_SIZE)/BLOCK_SIZE)
    y = random.randint(0, (self.h-BLOCK_SIZE)/BLOCK_SIZE)
    self.food = Point(x, y)
    if self.food in self.snake: # Generate food when eaten
        self.generate_food()

def collision(self):
    if pt is None: # Set pt to head
        pt = self.head
    if pt.x > pt.w - BLOCK_SIZE or pt.x < 0 or pt.y > pt.h - BLOCK_SIZE or pt.y < 0: # Out of bounds
        return True
    if pt in self.snake[1:]: # Head collides with body
        return True
    return False

def play_step(self, action):
    self.frame_iteration += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    self.move(action)
    self.snake.insert(0, self.head)
    game_over = False
    if self.collision() or self.frame_iteration > 100 * len(self.snake):
        game_over = True
        return game_over, self.score
    if self.head == self.food:
        self.score += 1
        self.generate_food()
    else:
        self.snake.pop()
    self.update_ui()
    self.clock.tick(SPEED)
    return game_over, self.score

def move(self, action):
    clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
    idx = clock_wise.index(self.direction)
    if np.array_equal(action, [1, 0, 0]): # Straight
        new_dir = clock_wise[idx]
    elif np.array_equal(action, [0, 1, 0]): # Right
        new_idx = (idx + 1) % 4
        new_dir = clock_wise[new_idx]
    self.direction = new_dir

    x = self.head.x
    y = self.head.y
    if self.direction == Direction.RIGHT:
        x += BLOCK_SIZE
    elif self.direction == Direction.LEFT:
        x -= BLOCK_SIZE
    elif self.direction == Direction.DOWN:
        y += BLOCK_SIZE
    elif self.direction == Direction.UP:
        y -= BLOCK_SIZE
    
    self.head = Point(x, y)