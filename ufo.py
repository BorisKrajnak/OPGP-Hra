import pygame
import json
import os
import sys
import random

# Inicializácia Pygame
pygame.init()

# Nastavenie rozlíšenia na celé okno
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hra - UFO")

# Načítanie konfiguračného súboru
with open("game_config.json", "r") as f:
    config = json.load(f)

map_image_name = config.get("map_image")

# Ak je vybraná posledná mapa (pozadie_vesmir_n12.jpg), vyber náhodnú mapu od n1 po n11
if map_image_name == "pozadie_vesmir_n12.jpg":
    random_index = random.randint(1, 11)
    map_image_name = f"pozadie_vesmir_n{random_index}.jpg"

map_path = os.path.join("img/map_imagines", map_image_name)

# Načítanie mapy alebo fallback
if os.path.exists(map_path):
    background = pygame.transform.scale(pygame.image.load(map_path), (width, height))
else:
    background = pygame.Surface((width, height))
    background.fill((0, 0, 0))

# Načítanie obrázka ovládania
control_image = pygame.image.load("img/ovladanie/ovladanie2.png")

# Zistenie rozmerov obrázka
control_rect = control_image.get_rect()

# Vypočítanie stredu obrazovky
control_rect.center = (width // 2, height // 2)

# Hlavný cyklus
running = True
while running:
    screen.blit(background, (0, 0))

    # Vykreslenie obrázka do stredu obrazovky
    screen.blit(control_image, control_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
