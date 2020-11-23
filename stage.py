import pygame
import json
import random
from game_object import Dirt, Coin, Heart
from enemies import Snake, Bird

bg = pygame.image.load('Webp.net-resizeimage (1).png')
stage_list = ['map4.json', 'map3.json', 'map2.json']


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class Stage:
    vel = 3

    def __init__(self, filename, cont_draw=True):
        self.filename = filename
        self.width = 13
        self.height = 19
        self.moveCount = 0
        self.cont_draw = cont_draw

        self.coin_group = pygame.sprite.Group()
        self.dirt_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.heart_group = pygame.sprite.Group()

        # Import stage from json file
        with open(self.filename) as f:
            data = json.load(f)
        self.stage = [x for x in chunks(data['layers'][1]['data'], self.width)]

        for row in range(self.height):
            for column in range(self.width):
                if self.stage[row][column] == 1 or self.stage[row][column] == 2:
                    self.dirt_group.add(Dirt(column * 32, row * 32 - 19 * 32 * self.cont_draw))
                elif self.stage[row][column] == 0.8:
                    self.coin_group.add(Coin(column * 32, row * 32 - 19 * 32 * self.cont_draw))
                elif self.stage[row][column] == 0.9:
                    self.heart_group.add(Heart(column * 32, row * 32 - 19 * 32 * self.cont_draw))
                elif self.stage[row][column] == 0.5:
                    self.enemies_group.add(Snake(column * 32, row * 32 - 20 - 19 * 32 * self.cont_draw))
                elif self.stage[row][column] == 0.6:
                    self.enemies_group.add(Bird(column * 32, row * 32 - 20 - 19 * 32 * self.cont_draw))

    def draw(self, win, player, current_dirt, current_enemies):
        self.dirt_group.update(self.vel, current_dirt)
        self.coin_group.update(self.vel, player)
        self.enemies_group.update(self.vel, current_enemies)
        self.heart_group.update(self.vel, player)

        self.dirt_group.draw(win)
        self.coin_group.draw(win)
        self.enemies_group.draw(win)
        self.heart_group.draw(win)

        self.moveCount += 1

    @classmethod
    def draw_many(cls, win, current_stage, player, current_dirt, current_enemies):
        if current_stage[0].vel * current_stage[0].moveCount >= 608 + 608 * current_stage[0].cont_draw:
            current_stage.append(Stage(random.choice(stage_list)))
            current_stage.pop(0)
        for stage in current_stage:
            stage.draw(win, player, current_dirt, current_enemies)
        return current_stage


stage1 = Stage('map.json', cont_draw=False)
stage2 = Stage(random.choice(stage_list))
current_stage = [stage1, stage2]
