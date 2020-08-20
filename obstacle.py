import pygame
import random
from defs import *


class Obstacle():

    def __init__(self, gameDisplay, x, y, obstacle_type):
        self.gameDisplay = gameDisplay
        self.state = OBSTACLE_MOVING
        self.obstacle_type = obstacle_type
        self.img = pygame.image.load(OBSTACLE_FILENAME)
        self.rect = self.img.get_rect()
        if obstacle_type == OBSTACLE_UPPER:
            y = y - self.rect.height
        self.set_position(x, y)

    def set_position(self, x, y):
        self.rect.left = x
        self.rect.top = y

    def move_position(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self):
        if self.rect.right < 0:
            self.state = OBSTACLE_DONE
            
    def update(self, dt, game_time):
        if self.state == OBSTACLE_MOVING:
            #self.move_position(-(OBSTACLE_SPEED + (game_time/99999) * dt), 0)
            self.move_position(-(OBSTACLE_SPEED * dt), 0)
            self.draw()
            self.check_status()

class ObstacleCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.obstacles = []


    def add_new_obstacle_pair(self, x):

        top_y = random.randint(OBSTACLE_MIN, OBSTACLE_MAX - OBSTACLE_GAP_SIZE)
        bottom_y = top_y + OBSTACLE_GAP_SIZE

        p1 = Obstacle(self.gameDisplay, x, top_y, OBSTACLE_UPPER)
        p2 = Obstacle(self.gameDisplay, x, bottom_y, OBSTACLE_LOWER)

        self.obstacles.append(p1)
        self.obstacles.append(p2)

    def create_new_set(self):
        self.obstacles = []
        placed = OBSTACLE_FIRST

        while placed < DISPLAY_W:
            self.add_new_obstacle_pair(placed)
            placed += OBSTACLE_ADD_GAP

    def update(self, dt, game_time):

        rightmost = 0

        for o in self.obstacles:
            o.update(dt, game_time)
            if o.obstacle_type == OBSTACLE_UPPER:
                if o.rect.left > rightmost:
                    rightmost = o.rect.left

        if rightmost < (DISPLAY_W - OBSTACLE_ADD_GAP):
            self.add_new_obstacle_pair(DISPLAY_W)

        self.obstacles = [o for o in self.obstacles if o.state == OBSTACLE_MOVING]

































































