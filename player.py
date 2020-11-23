import pygame
from enemies import Snake, Bird

damage_sound = pygame.mixer.Sound('damage.ogg')

walkLeft = [pygame.transform.scale(x, (40, 50)) for x in
            [pygame.image.load('tile004.png'), pygame.image.load('tile005.png'), pygame.image.load('tile006.png'),
             pygame.image.load('tile007.png')]]
walkRight = [pygame.transform.scale(x, (40, 50)) for x in
             [pygame.image.load('tile008.png'), pygame.image.load('tile009.png'), pygame.image.load('tile010.png'),
              pygame.image.load('tile011.png')]]
char = [pygame.transform.scale(x, (40, 50)) for x in
        [pygame.image.load('tile000.png'), pygame.image.load('tile001.png'), pygame.image.load('tile002.png'),
         pygame.image.load('tile003.png')]]

DEFAULT_JUMPCOUNT = 9
GRAVITY = 0.25


class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = char[0]
        self.rect = self.image.get_rect(x=x_pos, y=y_pos)
        self.score = 0
        self.life = 2

        self.vel = 8
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = DEFAULT_JUMPCOUNT
        self.movement = [self.vel, 0]
        self.isJump = False
        self.fallCount = 30
        self.time = 0
        self.collided = False

    # Check collision with enemies
    def enemies_collision(self, current_enemies):
        return pygame.sprite.spritecollide(self, current_enemies, False)

    # Check collision with dirt
    def collision_check(self, current_dirt):
        return pygame.sprite.spritecollide(self, current_dirt, False)

    # Check if jelly is on a tile
    def on_tile(self, collision):
        for tile in collision:
            if tile.rect.top - 15 <= self.rect.bottom <= tile.rect.top + 10 and not (
                    tile.rect.left > self.rect.right - 8 or tile.rect.right < self.rect.left + 8):
                self.rect.bottom = tile.rect.top
                return True
        return False

    # Check if jelly collided with enemies
    def enemies_collide(self, enemies_collision):
        if not self.collided:
            for enemy in enemies_collision:
                if not (not ((type(enemy) == Snake and enemy.rect.bottom + 10 < self.rect.bottom < enemy.rect.top) or (
                        type(enemy) == Bird and pygame.sprite.collide_rect_ratio(0.75)(self, enemy))) or (
                                enemy.rect.left > self.rect.right - 8 or enemy.rect.right < self.rect.left + 8)):
                    damage_sound.play()
                    self.collided = pygame.time.get_ticks()
                    self.life -= 1
        else:
            if pygame.time.get_ticks() - self.collided < 700:
                return
            else:
                self.collided = False

    def jump(self):
        self.isJump = True
        self.rect.y -= int(GRAVITY * (self.jumpCount ** 2))
        self.jumpCount -= 1
        if self.jumpCount <= 0:
            self.isJump = False
            self.jumpCount = DEFAULT_JUMPCOUNT

    def move(self, collision, enemies_collision):
        self.enemies_collide(enemies_collision)
        if not self.on_tile(collision):
            if self.isJump:
                self.jump()
            else:
                self.rect.y += int(GRAVITY * self.fallCount)
                self.fallCount += 5
                if self.fallCount > 50:
                    self.fallCount = 50
        else:
            self.jump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.movement[0]
            self.left = True
            self.right = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.movement[0]
            self.left = False
            self.right = True
        if self.rect.left < 0:
            self.rect.left = -6
        if self.rect.right > 416:
            self.rect.right = 422

    def draw(self, win):
        if self.walkCount + 1 > 12:
            self.walkCount = 0
        if self.left:
            if self.time % 3 == 0:
                self.image = walkLeft[self.walkCount % 4]
            if not (self.collided and self.time % 6 == 0):
                win.blit(self.image, self.rect)
            self.walkCount += 1
        elif self.right:
            if self.time % 3 == 0:
                self.image = walkRight[self.walkCount % 4]
            if not (self.collided and self.time % 6 == 0):
                win.blit(self.image, self.rect)
            self.walkCount += 1
        else:
            if self.time % 3 == 0:
                self.image = char[self.walkCount % 4]
            if not (self.collided and self.time % 3 == 0):
                win.blit(self.image, self.rect)
            self.walkCount += 1
        self.time += 1
