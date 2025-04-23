import os
import subprocess
import sys
import pygame
import time
import json

# Inicializácia Pygame
pygame.init()

# Nastavenie veľkosti okna na celú obrazovku
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Nastavenia hry")

# Farby
WHITE = (255, 255, 255)
DARK_GRAY = (169, 169, 169)
SPACE_BLUE = (10, 10, 40)
YELLOW = (255, 255, 0)
PURPLE = (31, 10, 30)

def draw_vertical_gradient(surface, top_color, bottom_color):
    for y in range(surface.get_height()):
        ratio = y / surface.get_height()
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

# Fonty
font_path = "Font/VOYAGER.ttf"  # cesta k fontu
loading_font = pygame.font.Font(font_path, 200)
font = pygame.font.Font(None, 50)

# Settings
draw_vertical_gradient(screen, SPACE_BLUE, PURPLE)
loading_text = loading_font.render("LOADING", True, WHITE)
screen.blit(loading_text, (
    width // 2 - loading_text.get_width() // 2,
    height // 2 - loading_text.get_height() // 2
))
pygame.display.flip()

# Cesta k obrázkom
MAPS_FOLDER = r"img/map_imagines"
CONTROLS_FOLDER = r"img/ovladanie"

# Načítanie 12 obrázkov (máp)
map_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(MAPS_FOLDER, f"pozadie_vesmir_n{i}.jpg")), (150, 90))
    if os.path.exists(os.path.join(MAPS_FOLDER, f"pozadie_vesmir_n{i}.jpg"))
    else pygame.Surface((150, 90)) for i in range(1, 13)
]

# Načítanie obrázkov raketiek
control_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(CONTROLS_FOLDER, f"ovladanie{i + 1}.png")), (160, 90))
    if os.path.exists(os.path.join(CONTROLS_FOLDER, f"ovladanie{i + 1}.png"))
    else pygame.Surface((160, 90)) for i in range(3)
]

# Rozloženie máp a ovládania
map_positions = [
    (width // 2 - 540 + (i % 6) * 180, height // 2 - 240 + (i // 6) * 110) for i in range(12)
]
control_positions = [
    (width // 2 - 280, height // 2 + 120),
    (width // 2 - 80, height // 2 + 120),
    (width // 2 + 120, height // 2 + 120)
]

selected_map = None
selected_control = None

# Tlačidlá
button_width, button_height, border_radius = 250, 50, 20
start_button = pygame.Rect(width - button_width - 40, height - button_height - 40, button_width, button_height)
back_button = pygame.Rect(40, height - button_height - 40, button_width, button_height)

# Funkcia na spustenie hry
def start_game(selected_control, selected_map):
    map_data = {
        "map_image": f"pozadie_vesmir_n{selected_map + 1}.jpg"
    }
    with open("game_config.json", "w") as f:
        json.dump(map_data, f)

    script_map = {
        0: "raketka.py",
        1: "ufo.py",
        2: "omniman.py"
    }
    script_to_run = script_map.get(selected_control)
    if script_to_run:
        subprocess.Popen(["python", script_to_run], creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(1)
        pygame.quit()
        sys.exit()

# Hlavný cyklus
running = True
while running:
    draw_vertical_gradient(screen, SPACE_BLUE, PURPLE)

    # Tlačidlá
    pygame.draw.rect(screen, DARK_GRAY, start_button, border_radius=border_radius)
    pygame.draw.rect(screen, DARK_GRAY, back_button, border_radius=border_radius)
    screen.blit(font.render("START", True, WHITE), font.render("START", True, WHITE).get_rect(center=start_button.center))
    screen.blit(font.render("BACK", True, WHITE), font.render("BACK", True, WHITE).get_rect(center=back_button.center))

    # Nadpisy
    screen.blit(font.render("NASTAVENIA HRY", True, WHITE), (width // 2 - 160, 50))
    screen.blit(font.render("VÝBER MAPY:", True, WHITE), (width // 2 - 120, 110))
    screen.blit(font.render("VÝBER RAKETKY:", True, WHITE), (width // 2 - 140, height // 2 + 70))

    # Mapa a raketky
    for i, pos in enumerate(map_positions):
        color = YELLOW if selected_map == i else WHITE
        pygame.draw.rect(screen, color, (pos[0] - 5, pos[1] - 5, 160, 100), 5)
        screen.blit(map_images[i], pos)

    for i, pos in enumerate(control_positions):
        color = YELLOW if selected_control == i else WHITE
        pygame.draw.rect(screen, color, (pos[0] - 5, pos[1] - 5, 170, 100), 5)
        screen.blit(control_images[i], pos)

    # Udalosti
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                subprocess.Popen(["python", "uvodne_okno.py"], creationflags=subprocess.CREATE_NO_WINDOW)
                time.sleep(0.5)
                running = False
            if start_button.collidepoint(event.pos) and selected_map is not None and selected_control is not None:
                start_game(selected_control, selected_map)

            for i, pos in enumerate(map_positions):
                rect = pygame.Rect(pos[0], pos[1], 150, 90)
                if rect.collidepoint(event.pos):
                    selected_map = i

            for i, pos in enumerate(control_positions):
                rect = pygame.Rect(pos[0], pos[1], 160, 90)
                if rect.collidepoint(event.pos):
                    selected_control = i

    pygame.display.flip()

pygame.quit()
sys.exit()
