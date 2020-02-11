import pygame
from pygame import Color
import os
import sys


FPS = 50
WIDTH = 400
HEIGHT = 300


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def get_shift(self):
        return self.rect.x, self.rect.y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
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


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
    
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)

        global cur_level, player, tile_width, tile_height
        level = load_level(levels[cur_level])

        def update_level(x_axis):
            tiles_group.empty()

            with open('data/' + levels[cur_level], 'w') as f:
                for line in level:
                    f.write(line + '\n')

            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level[y][x] == '.':
                        Tile('empty', x - 1, y - 1)
                    elif level[y][x] == '#':
                        Tile('wall', x - 1, y - 1)
                    elif level[y][x] == '@':
                        Tile('empty', x - 1, y - 1)

            for tile in tiles_group:
                if x_axis:
                    tile.rect.y += old_dy
                else:
                    tile.rect.x += old_dx

        old_dx, old_dy = tiles_group.sprites()[len(level[0]) + 1].get_shift()

        if old_dy > tile_height:
            level = [level[-1]] + level[:-1]
            update_level(False)
        elif old_dy < -tile_height: 
            level = level[1:] + [level[0]]
            update_level(False)
        if old_dx > tile_width:
            copy_level = level.copy()
            for i in range(len(level)):
                copy_level[i] = level[i][-1] + level[i][:-1]
            level = copy_level
            update_level(True)
        elif old_dx < -tile_width:
            copy_level = level.copy()
            for i in range(len(level)):
                copy_level[i] = level[i][1:] + level[i][0]
            level = copy_level
            update_level(True)

        player.rect.x += self.dx
        player.rect.y += self.dy
        for tile in tiles_group:
            tile.rect.x += self.dx
            tile.rect.y += self.dy


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
                Tile('empty', x, y - 1)
            elif level[y][x] == '#':
                Tile('wall', x, y - 1)
            elif level[y][x] == '@':
                Tile('empty', x, y - 1)
                new_player = Player(x, y)           
    return new_player, x - 1, y - 1


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


levels = ['map.txt']
cur_level = 0
for param in sys.argv:
    if param.endswith('.txt'):
        levels.append(param)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
start_screen()

tile_width = tile_height = 50
tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mario.png', -1)
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player, WIDTH, HEIGHT = generate_level(load_level('map.txt'))
camera = Camera()

WIDTH *= (tile_width) 
HEIGHT *= (tile_height)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                try:
                    cur_level += 1
                    if cur_level >= len(levels):
                        cur_level = 0
                        tiles_group.empty()
                        player_group.empty()
                        player, WIDTH, HEIGHT = generate_level(load_level(levels[cur_level]))
                        WIDTH *= tile_width
                        HEIGHT *= tile_height
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                except Exception:
                    print('Неверное название файлов')
                    running = False
                    break
    else:
        clock.tick(FPS)
        player_group.update()
        screen.fill(Color('black'))
        camera.update(player)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
