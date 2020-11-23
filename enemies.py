import pygame

snakeRight = [pygame.image.load('snake0.png'), pygame.image.load('snake1.png'), pygame.image.load('snake2.png'),
              pygame.image.load('snake3.png')]
snakeLeft = [pygame.image.load('snake4.png'), pygame.image.load('snake5.png'), pygame.image.load('snake6.png'),
             pygame.image.load('snake7.png')]
birdRight = [pygame.image.load('bird0.png'), pygame.image.load('bird1.png'), pygame.image.load('bird2.png'),
             pygame.image.load('bird3.png')]
birdLeft = [pygame.image.load('bird4.png'), pygame.image.load('bird5.png'), pygame.image.load('bird6.png'),
            pygame.image.load('bird7.png')]


class Snake(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.vel = 3
        self.left = True
        self.right = False
        self.image = snakeLeft[0]
        self.rect = self.image.get_rect(x=x_pos, y=y_pos + 40)
        self.walkCount = 0
        self.rect.height -= 40

    def update(self, incre, current_enemies):
        if self.walkCount > 34:
            if self.left:
                self.left = False
                self.right = True
                self.walkCount = 0
            elif self.right:
                self.left = True
                self.right = False
                self.walkCount = 0
        if self.left:
            self.rect.x -= self.vel
            self.image = snakeLeft[self.walkCount % 4]
            self.walkCount += 1
        elif self.right:
            self.rect.x += self.vel
            self.image = snakeRight[self.walkCount % 4]
            self.walkCount += 1
        self.rect.y += incre
        if self.rect.colliderect(pygame.Rect(0, 0, 416, 608)):
            current_enemies.add(self)


class Bird(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = birdRight[0]
        self.rect = self.image.get_rect(x=x_pos, y=y_pos + 10)
        self.vel = 5
        self.left = False
        self.right = True
        self.walkCount = 0

    def update(self, incre, current_enemies):
        if self.walkCount > 90:
            if self.left:
                self.left = False
                self.right = True
                self.walkCount = 0
            elif self.right:
                self.left = True
                self.right = False
                self.walkCount = 0
        if self.left:
            self.rect.x -= self.vel
            self.image = birdLeft[self.walkCount % 4]
            self.walkCount += 1
        elif self.right:
            self.rect.x += self.vel
            self.image = birdRight[self.walkCount % 4]
            self.walkCount += 1
        self.rect.y += incre
        if self.rect.colliderect(pygame.Rect(0, 0, 416, 608)):
            current_enemies.add(self)
