import pygame
from pygame import Color
import os
import sys


FPS = 50
WIDTH = 400
HEIGHT = 300


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self):
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.x += 5
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.x -= 5
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.rect.y += 5
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.rect.y -= 5

    
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
   
    max_width = max(map(len, level_map))   
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)           
    return new_player, x + 1, y + 1


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["OMEGA GIGA SUPER MARIO ODESSY", "",
                  "Правила игры:",
                  "Нажимайте стрелки чтобы двигаться,", "",
                  "Нажмите любую кнопку чтобы начать"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    clock = pygame.time.Clock()
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
start_screen()

tile_width = tile_height = 50
tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mario.png', -1)
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player, WIDTH, HEIGHT = generate_level(load_level('map.txt'))

WIDTH *= tile_width
HEIGHT *= tile_height

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player_group.update()
    clock.tick(FPS)
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
