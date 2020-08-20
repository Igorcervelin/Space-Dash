import pygame
import random
from defs import *
from net import Net
import numpy as np

class Ship():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.state = SHIP_ALIVE
        self.img = pygame.image.load(SHIP_FILENAME)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.net = Net(NET_INPUTS, NET_HIDDEN, NET_OUTPUTS)
        self.set_position(SHIP_START_X, SHIP_START_Y)

    def reset(self):
        self.state = SHIP_ALIVE
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.set_position(SHIP_START_X, SHIP_START_Y)

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, dt):

        distance = 0
        new_speed = 0

        distance = (self.speed * dt) + (0.5 * GRAVITY * dt * dt)
        new_speed = self.speed + (GRAVITY * dt)

        self.rect.centery += distance
        self.speed = new_speed

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0

    def jump(self, obstacles):
        inputs = self.get_inputs(obstacles)
        val = self.net.get_max_value(inputs)
        if val > JUMP_CHANCE:
            self.speed = SHIP_START_SPEED

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self, obstacles):
        if self.rect.bottom > DISPLAY_H:
            self.state = SHIP_DEAD
        else:
            self.check_hits(obstacles)

    def assign_collision_fitness(self, o):
        gap_y = 0
        if o.obstacle_type == OBSTACLE_UPPER:
            gap_y = o.rect.bottom + OBSTACLE_GAP_SIZE / 2
        else:
            gap_y = o.rect.top - OBSTACLE_GAP_SIZE / 2

        self.fitness = -(abs(self.rect.centery - gap_y))

    def check_hits(self, obstacles):
        for o in obstacles:
            if o.rect.colliderect(self.rect):
                self.state = SHIP_DEAD
                self.assign_collision_fitness(o)
                break

    def update(self, dt, obstacles):
        if self.state == SHIP_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.jump(obstacles)
            self.draw()
            self.check_status(obstacles)


    def get_inputs(self, obstacles):

        closest = DISPLAY_W * 2 
        bottom_y = 0  
        for o in obstacles:
            if o.obstacle_type == OBSTACLE_UPPER and o.rect.right < closest and o.rect.right > self.rect.left:
                closest = o.rect.right
                bottom_y = o.rect.bottom


        horizontal_distance = closest - self.rect.centerx
        vertical_distance = (self.rect.centery) - (bottom_y + OBSTACLE_GAP_SIZE / 2)

        inputs = [
            ((horizontal_distance / DISPLAY_W) * 0.99) + 0.01,
            ((( vertical_distance + Y_SHIFT) / NORMALIZER ) * 0.99 ) + 0.01
        ]

        return inputs

    def create_offspring(p1, p2, gameDisplay):
        new_ship = Ship(gameDisplay)
        new_ship.net.create_mixed_weights(p1.net, p2.net)
        return new_ship
        

class ShipCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.ships = []
        self.create_new_generation()

    def create_new_generation(self):
        self.ships = []
        for i in range(0, GENERATION_SIZE):
            self.ships.append(Ship(self.gameDisplay))

    def update(self, dt, obstacles):
        num_alive = 0
        for s in self.ships:
            s.update(dt, obstacles)
            if s.state == SHIP_ALIVE:
                num_alive += 1

        return num_alive

    def evolve_population(self):

        for s in self.ships:
            s.fitness += s.time_lived * OBSTACLE_SPEED

        self.ships.sort(key=lambda x: x.fitness, reverse=True)

        cut_off = int(len(self.ships) * MUTATION_CUT_OFF)
        good_ships = self.ships[0:cut_off]
        bad_ships = self.ships[cut_off:]
        num_bad_to_take = int(len(self.ships) * MUTATION_BAD_TO_KEEP)

        for s in bad_ships:
            s.net.modify_weights()

        new_ships = []

        idx_bad_to_take = np.random.choice(np.arange(len(bad_ships)), num_bad_to_take, replace=False)

        for index in idx_bad_to_take:
            new_ships.append(bad_ships[index])

        new_ships.extend(good_ships)

        children_needed = len(self.ships) - len(new_ships)

        while len(new_ships) < len(self.ships):
            idx_to_breed = np.random.choice(np.arange(len(good_ships)), 2, replace=False)
            if idx_to_breed[0] != idx_to_breed[1]:
                new_ship = Ship.create_offspring(good_ships[idx_to_breed[0]], good_ships[idx_to_breed[1]], self.gameDisplay)
                if random.random() < MUTATION_MODIFY_CHANCE_LIMIT:
                    new_ship.net.modify_weights()
                new_ships.append(new_ship)

        for s in new_ships:
            s.reset();

        self.ships = new_ships

















