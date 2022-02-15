import pygame

pygame.mixer.init()
from player import Player
from stage import Stage
import stage
import random
from moviepy.editor import VideoFileClip


class Game:
    def __init__(self):
        self.small_font = pygame.font.Font('Jura-Light.ttf', 28)
        self.icon = pygame.image.load('images/icon.png')
        self.heart = pygame.image.load('images/heart.png')
        self.bg = pygame.image.load('images/Webp.net-resizeimage (1).png')
        self.game_over = pygame.mixer.Sound('sound/game_over.wav')
        self.win = pygame.display.set_mode((416, 608))
        pygame.display.set_caption('Jelly Jump')
        pygame.display.set_icon(self.icon)

        self.clock = pygame.time.Clock()
        self.current_dirt = pygame.sprite.Group()
        self.current_enemies = pygame.sprite.Group()
        self.running = True
        self.jelly = Player(288, 450)
        self.quit = False
        with open('high_score.txt') as hs:
            self.high_score = int(hs.read())

    def new_game(self):
        self.running = True
        self.jelly = Player(160, 475)
        self.jelly.score = 0
        stage.current_stage = [Stage('map/map.json', cont_draw=False), Stage(random.choice(stage.stage_list))]

    def start(self):
        clip = VideoFileClip('video/Press any key to start.mp4')
        clip.preview()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    self.running = True
                    waiting = False

    def run(self):
        self.new_game()
        while self.running:

            self.clock.tick(17)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit = True
            self.win.blit(self.bg, (0, 0))

            # Stage drawing and update; dirt and enemies collision check
            self.current_dirt.empty()
            self.current_enemies.empty()
            stage.current_stage = Stage.draw_many(self.win, stage.current_stage, self.jelly, self.current_dirt,
                                                  self.current_enemies)
            dirt_collision = self.jelly.collision_check(self.current_dirt)
            enemies_collision = self.jelly.enemies_collision(self.current_enemies)

            # Move and draw the jelly, íts score and heart
            self.jelly.move(dirt_collision, enemies_collision)
            self.jelly.draw(self.win)
            text = self.small_font.render(str(self.jelly.score), False, (0, 0, 0))
            self.win.blit(text, (15, 15))
            for heart in range(self.jelly.life):
                self.win.blit(self.heart, (15 + heart * 25, 50))
            pygame.display.update()

            # Losing condition
            if self.jelly.rect.top > 608 or self.jelly.life <= 0:
                self.running = False

    def end(self):
        if self.quit:
            return
        self.game_over.play()
        clip2 = VideoFileClip('video/Press any key to restart.mp4')
        clip2.preview()
        jelly_score = self.small_font.render(str(self.jelly.score), False, (0, 0, 0))
        if self.jelly.score > self.high_score:
            self.high_score = self.jelly.score
            with open('high_score.txt', 'w') as hs:
                hs.write(str(self.jelly.score))
        high_score = self.small_font.render(str(self.high_score), False, (0, 0, 0))
        self.win.blit(jelly_score, (185, 355))
        self.win.blit(high_score, (185, 490))
        pygame.display.update()
        self.wait_for_key()
