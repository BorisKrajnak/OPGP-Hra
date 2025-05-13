import json
import pygame
import sys
import os
import random
import subprocess
import time

from vyber_pozadia import nacitaj_pozadie


# Funkcia na uloženie aktívnej hry do JSON
def save_game_config(game_name):
    # Skontroluj, či súbor existuje
    if not os.path.exists("game_config.json"):
        # Ak neexistuje, vytvor nový súbor s default hodnotou
        config = {"active_game": game_name}
        with open("game_config.json", "w") as f:
            json.dump(config, f, indent=4)
    else:
        # Ak súbor existuje, načítaj aktuálne nastavenia a uprav hodnotu
        with open("game_config.json", "r") as f:
            config = json.load(f)

        config["active_game"] = game_name  # Uprav hodnotu aktívnej hry

        # Ulož upravený config späť do súboru
        with open("game_config.json", "w") as f:
            json.dump(config, f, indent=4)


# Inicializácia Pygame
pygame.init()

# Celá obrazovka
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("UFO")

# UFO parametre
ufo_x = width // 2
ufo_y = height // 2
ufo_speed = 0
gravity = 0.5
jump_strength = -10
move_speed = 5

# Načítanie pozadia
background = nacitaj_pozadie("game_config.json", width, height)

# Slovník na cache obrázkov
loaded_images = {}

# Načítanie animácie UFO
def nacitaj_animaciu(cesta, x, y, scale=0.25):
    frames = []
    for filename in sorted(os.listdir(cesta)):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            if filename not in loaded_images:
                image = pygame.image.load(os.path.join(cesta, filename)).convert_alpha()
                new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
                image = pygame.transform.scale(image, new_size)
                loaded_images[filename] = image
            rect = loaded_images[filename].get_rect(center=(x, y))
            frames.append((loaded_images[filename], rect))
    return frames

ufo_frames = nacitaj_animaciu("img/ufo_frames", ufo_x, ufo_y)
image, _ = ufo_frames[0]
ufo_width, ufo_height = image.get_width(), image.get_height()

# Načítanie meteor obrázka
meteor_image = pygame.image.load(os.path.join("img", "prekazky", "meteor2.png")).convert_alpha()

class Meteor:
    def __init__(self):
        self.size = random.randint(40, 100)
        original = pygame.transform.scale(meteor_image, (self.size, self.size))
        self.image = pygame.transform.rotate(original, -45)  # otočenie obrázka
        self.x = width + self.image.get_width()
        self.y = random.randint(0, height - self.image.get_height())
        self.speed = random.uniform(3.0, 8.0)
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.x -= self.speed
        self.rect.x = int(self.x)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.x + self.image.get_width() < 0


# Animácia UFO
frame_index = 0
frame_delay = 70
last_update = pygame.time.get_ticks()

# Meteority
meteory = []
spawn_delay = 1200
last_spawn_time = pygame.time.get_ticks()

running = True
clock = pygame.time.Clock()

# Ulož aktuálnu hru do JSON pred začiatkom
save_game_config("ufo")

while running:
    screen.blit(background, (0, 0))

    # Udalosti
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            ufo_speed = jump_strength

    # Klávesy
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        ufo_x -= move_speed
    if keys[pygame.K_d]:
        ufo_x += move_speed

    # Fyzika
    ufo_speed += gravity
    ufo_y += ufo_speed

    # Obmedzenia
    ufo_x = max(0, min(ufo_x, width - ufo_width))
    ufo_y = max(0, min(ufo_y, height - ufo_height))
    if ufo_y == height - ufo_height:
        ufo_speed = 0

    # UFO animácia
    current_time = pygame.time.get_ticks()
    if current_time - last_update > frame_delay:
        frame_index = (frame_index + 1) % len(ufo_frames)
        last_update = current_time

    current_ufo_image = ufo_frames[frame_index][0]
    screen.blit(current_ufo_image, (ufo_x, ufo_y))
    ufo_rect = current_ufo_image.get_rect(topleft=(ufo_x, ufo_y))
    ufo_mask = pygame.mask.from_surface(current_ufo_image)

    # Spawn meteoritov
    if current_time - last_spawn_time > spawn_delay:
        meteory.append(Meteor())
        last_spawn_time = current_time

    # Meteor update a kolízia
    for meteor in meteory[:]:
        meteor.update()
        if meteor.is_off_screen():
            meteory.remove(meteor)
            continue

        offset = (int(meteor.x - ufo_rect.left), int(meteor.y - ufo_rect.top))
        if ufo_mask.overlap(meteor.mask, offset):
            subprocess.Popen(["python", "game_over.py"], creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(0.5)
            running = False
            pygame.quit()
            sys.exit()

        meteor.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
