import pygame
from game import Game

if __name__ == '__main__':
    pygame.init()
    g = Game()
    g.start()
    while g.running:
        g.run()
        g.end()
    pygame.quit()

