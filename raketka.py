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

# Nastavenie rozlíšenia na celé okno
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Raketka")
clock = pygame.time.Clock()

# Načítanie pozadia
background = nacitaj_pozadie("game_config.json", width, height)

# Parametre raketky
player_width, player_height = 120, 120
player_speed = 10

# Načítanie snímkov animácie
player_frames = []
gif_folder = os.path.join("img", "raketka_frames")  # aktualizovaná cesta
frame_rate = 100
last_frame_time = pygame.time.get_ticks()
current_frame = 0

# Načítanie a otočenie snímkov
for filename in sorted(os.listdir(gif_folder)):
    frame = pygame.image.load(os.path.join(gif_folder, filename))
    frame = pygame.transform.scale(frame, (player_width, player_height))
    frame = pygame.transform.rotate(frame, -45)
    player_frames.append(frame)

# Načítanie obrázka meteoritu
meteor_image = pygame.image.load(os.path.join("img", "prekazky", "meteor.png")).convert_alpha()

# Trieda Meteor
class Meteor:
    def __init__(self):
        self.size = random.randint(40, 100)
        self.image = pygame.transform.scale(meteor_image, (self.size, self.size))
        self.x = width + self.size
        self.y = random.randint(0, height - self.size)
        self.speed = random.uniform(3.0, 8.0)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.x -= self.speed
        self.rect.x = int(self.x)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.x + self.size < 0

# Hlavná hra
def spusti_hru():
    global current_frame, last_frame_time

    player_x, player_y = width // 2, height // 2
    current_frame = 0
    last_frame_time = pygame.time.get_ticks()

    meteory = []
    spawn_delay = 1200
    last_spawn_time = pygame.time.get_ticks()
    running = True

    # Hlavný cyklus
    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        rotation_angle = 0
        if keys[pygame.K_w]:
            rotation_angle = +45
            player_y -= player_speed
        elif keys[pygame.K_s]:
            rotation_angle = -45
            player_y += player_speed
        else:
            rotation_angle = 0

        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed

        # Obmedzenie pohybu na základe stredu raketky
        half_width = player_width // 2
        half_height = player_height // 2
        player_x = max(half_width, min(player_x, width - half_width))
        player_y = max(half_height - 30, min(player_y, height - half_height + 30))

        # Animácia raketky
        if pygame.time.get_ticks() - last_frame_time > frame_rate:
            current_frame = (current_frame + 1) % len(player_frames)
            last_frame_time = pygame.time.get_ticks()

        # Spawn meteorov
        if pygame.time.get_ticks() - last_spawn_time > spawn_delay:
            meteory.append(Meteor())
            last_spawn_time = pygame.time.get_ticks()

        # Kreslenie scény
        rotated_frame = pygame.transform.rotate(player_frames[current_frame], rotation_angle)
        frame_rect = rotated_frame.get_rect(center=(player_x, player_y))
        player_mask = pygame.mask.from_surface(rotated_frame)

        for meteor in meteory[:]:
            meteor.update()
            if meteor.is_off_screen():
                meteory.remove(meteor)
                continue

            offset = (int(meteor.x - frame_rect.left), int(meteor.y - frame_rect.top))
            if player_mask.overlap(meteor.mask, offset):
                subprocess.Popen(["python", "game_over.py"],
                                 creationflags=subprocess.CREATE_NO_WINDOW)  # Toto potlačí okno príkazového riadku
                time.sleep(0.5)
                running = False
                pygame.quit()
                sys.exit()

            meteor.draw(screen)

        # Kreslenie raketky
        screen.blit(rotated_frame, frame_rect.topleft)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    save_game_config("raketka")
    spusti_hru()
