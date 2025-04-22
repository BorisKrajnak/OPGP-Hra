import pygame
import os
import json
import random

def nacitaj_pozadie(config_file, screen_width, screen_height):
    # Načítanie json súbora
    with open(config_file, "r") as f:
        config = json.load(f)

    map_image_name = config.get("map_image")
    # Výber náhodnej mapy a konkrétnej mapy
    if map_image_name == "pozadie_vesmir_n12.jpg":
        random_index = random.randint(1, 11)
        map_image_name = f"pozadie_vesmir_n{random_index}.jpg"

    # Zobrazenie pozadia
    map_path = os.path.join("img/map_imagines", map_image_name)
    if os.path.exists(map_path):
        return pygame.transform.scale(pygame.image.load(map_path), (screen_width, screen_height))
    else:
        surface = pygame.Surface((screen_width, screen_height))
        surface.fill((0, 0, 0))
        return surface

def nacitaj_obrazok(image_path, center_x, center_y):
    if os.path.exists(image_path):
        image = pygame.image.load(image_path)
        rect = image.get_rect()
        rect.center = (center_x, center_y)
        return image, rect
    else:
        raise FileNotFoundError(f"Nenašiel sa súbor {image_path}")