import pygame
vec = pygame.math.Vector2

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
GRAY = 192,192,192
RED = 255, 0, 0

PLAYER_ACC = 10
PLAYER_GRAV = .7

size = WIDTH, HEIGHT = 1000, 500
START_POS = 40, HEIGHT/2
PLATFORM_HEIGHT = 60

FPS = 30

platform_list = [
    [0, HEIGHT - 80, 80, PLATFORM_HEIGHT],
    [160, HEIGHT-100, 80, PLATFORM_HEIGHT],
    [320, HEIGHT-120, 80, PLATFORM_HEIGHT],
    [480, HEIGHT-140, 80, PLATFORM_HEIGHT],
    [640, HEIGHT-160, 80, PLATFORM_HEIGHT],
    [900, HEIGHT-180, 80, PLATFORM_HEIGHT]
]

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Game!")
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        self.player = Player()
        for i in platform_list:
            p = Platform(i[0], i[1], i[2], i[3])
            self.platforms.add(p)
            self.all_sprites.add(p)
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top + 2
            self.player.vel.y = 0

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)


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

game = Game()
game.new()
