import pygame
import sprites
vec = pygame.math.Vector2

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
GRAY = 192,192,192
RED = 255, 0, 0

size = WIDTH, HEIGHT = 1000, 500

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

        self.player = sprites.Player()
        for i in platform_list:
            p = sprites.Platform(i[0], i[1], i[2], i[3])
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


game = Game()
game.new()
