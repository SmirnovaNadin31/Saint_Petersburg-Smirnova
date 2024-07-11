import pygame
import sys
import os


WIND_SIZE = WIDTH, HEIGHT = 11 * 50, 11 * 50
all_sprites = pygame.sprite.Group()
tiles_sprites = pygame.sprite.Group()
hero_sprites = pygame.sprite.Group()
player = None

def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_window(screen):
    image_fon = pygame.transform.scale(load_image('fon_1.jpg'), (WIDTH, HEIGHT))
    screen.blit(image_fon, (0, 0))
    title_text = ["Hello!", "",
                  "I am glad to you",
                  "Excellent!!!"]
    text_size = pygame.font.Font(None, 50)
    y = 250
    for line in title_text:
        text = text_size.render(line, True, pygame.Color("green"))
        x = 10
        y += text.get_rect().height + 10
        screen.blit(text, (x, y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()

def load_level(name):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"{fullname} не найден\n, выберите labirint.txt, map2.txt, map3.txt")
        sys.exit()
    try:
        with open(fullname) as f_map:
            map_list = [x.strip() for x in f_map]
        if map_list:
            max_len = max(map(len, map_list))
            print(map_list, max_len)
        else:
            max_len = 11
            map_list = ['.'] * 10 + ['@']

        map_list = [x.ljust(max_len, '.') for x in map_list]
        return map_list
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise



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
                new_player = Hero(x, y)
    return new_player, x, y

class Hero(pygame.sprite.Sprite):
    image_hero = None
    tile_width, tile_height = 50, 50
    def __init__(self, x, y):
        super().__init__(hero_sprites, all_sprites)
        if Hero.image_hero is None:
            Hero.image_hero = load_image('mar.png')
        self.image = Hero.image_hero
        self.rect = self.image_hero.get_rect().move(
            x * Tile.tile_width + 10, y * Tile.tile_height + 15)
        self.x = x
        self.y = y

    def mover(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect = self.rect.move(dx * Tile.tile_width, dy * Tile.tile_height)


class Tile(pygame.sprite.Sprite):
    image = None
    tile_width, tile_height = 50, 50

    def __init__(self, type_tile, x, y):
        super().__init__(tiles_sprites, all_sprites)
        if type_tile == 'empty':
            Tile.image = load_image('grass.png')
        elif type_tile == 'wall':
            Tile.image = load_image('box.png')
        self.image = Tile.image
        self.rect = self.image.get_rect().move(
            x * Tile.tile_width, y * Tile.tile_height)


def move(name, player, par):
    x, y = player.x, player.y
    print(x, y)
    plan = load_level(name)
    print(plan, len(plan[0]), len(plan))
    if 0 <= x <= len(plan[0]) and 0 <= y <= len(plan):
        if par == 'up':
            if y - 1 >= 0 and (plan[y - 1][x] == '.' or plan[y - 1][x] == '@'):
                player.mover(0, -1)
        elif par == 'down':
            if y + 1 < len(plan) and (plan[y + 1][x] == '.' or plan[y + 1][x] == '@'):
                player.mover(0, 1)
        elif par == 'left':
            if x - 1 >= 0 and (plan[y][x - 1] == '.' or plan[y][x - 1] == '@'):
                player.mover(-1, 0)
        elif par == 'right':
            if x + 1 < len(plan[0]) and (plan[y][x + 1] == '.' or plan[y][x + 1] == '@'):
                player.mover(1, 0)



def main():
    pygame.init()
    print('Выберите уровень: labirint.txt, map2.txt, map3.txt, map3')
    name = input()
    screen = pygame.display.set_mode(WIND_SIZE)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Tiles')
    start_window(screen)
    player, level_x, level_y = generate_level(load_level(name))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(name, player, 'up')
                if event.key == pygame.K_DOWN:
                    move(name, player, 'down')
                if event.key == pygame.K_LEFT:
                    move(name, player, 'left')
                if event.key == pygame.K_RIGHT:
                    move(name, player, 'right')
        screen.fill((102, 25, 89))
        all_sprites.draw(screen)
        hero_sprites.draw(screen)
        clock.tick(40)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()


