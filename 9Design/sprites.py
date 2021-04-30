import pygame
vec = pygame.math.Vector2

size = WIDTH, HEIGHT = 1000, 500
PLAYER_ACC = 10
PLAYER_GRAV = .7
START_POS = 40, HEIGHT/2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("character.png")
        self.image = pygame.transform.smoothscale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (START_POS)
        self.pos = vec(START_POS)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.jumping = False
        self.jumpCount = 8
        self.jumpCountNormal = self.jumpCount

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pos.x -= PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.pos.x += PLAYER_ACC

        if not self.jumping:
            if keys[pygame.K_SPACE] and self.pos.y > 0:
                self.jumping = True
        else:
            if self.jumpCount >= (0 - self.jumpCountNormal):
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.pos.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.jumping = False
                self.jumpCount = self.jumpCountNormal

        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("platform.png")
        #self.image = pygame.transform.smoothscale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x