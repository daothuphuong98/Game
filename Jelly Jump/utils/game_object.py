import pygame


class Dirt(pygame.sprite.Sprite):
    image = pygame.image.load('images/jelly/Tile_02.png')

    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.rect = Dirt.image.get_rect(x=x_pos, y=y_pos)

    def update(self, incre, current_dirt):
        self.rect.y += incre
        if self.rect.colliderect(pygame.Rect(0, 0, 416, 608)):
            current_dirt.add(self)


class Coin(pygame.sprite.Sprite):
    image = pygame.image.load('images/coin.png')
    sound = pygame.mixer.Sound('sound/coin.wav')

    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.rect = Dirt.image.get_rect(x=x_pos, y=y_pos)

    def update(self, incre, player):
        if pygame.sprite.collide_rect_ratio(0.4)(self, player):
            self.sound.play()
            self.kill()
            player.score += 10
        self.rect.y += incre


class Heart(pygame.sprite.Sprite):
    image = pygame.image.load('images/heart.png')
    sound = pygame.mixer.Sound('sound/heart.wav')

    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.rect = Dirt.image.get_rect(x=x_pos, y=y_pos)

    def update(self, incre, player):
        if pygame.sprite.collide_rect_ratio(0.4)(self, player):
            self.sound.play()
            self.kill()
            player.life += 1
            if player.life > 2:
                player.life = 2
        self.rect.y += incre
