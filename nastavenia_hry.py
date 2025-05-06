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

# Načítanie vlastného fontu pre nadpis (názov hry)
font_path = "Font/VOYAGER.ttf"  # cesta k fontu
font_size = 50  # veľkosť písma
custom_font = pygame.font.Font(font_path, font_size)

def draw_vertical_gradient(surface, top_color, bottom_color):
    for y in range(surface.get_height()):
        ratio = y / surface.get_height()
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))


def draw_gradient_button(surface, rect, color1, color2, text, font, text_color):
    # Gradient výplň s rounded corners
    button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    for y in range(rect.height):
        ratio = y / rect.height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(button_surf, (r, g, b), (0, y), (rect.width, y))

    # Vykreslenie rounded rect s gradientom
    mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255), (0, 0, rect.width, rect.height), border_radius=7)
    button_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # Vykreslenie tlačidla na hlavnú obrazovku
    surface.blit(button_surf, (rect.x, rect.y))

    # BIELY OBRYS (border)
    pygame.draw.rect(surface, WHITE, rect, width=3, border_radius=7)

    # Text v strede
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)



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
map_images = []
for i in range(1, 13):
    image = None
    for ext in [".png", ".jpg"]:
        path = os.path.join(MAPS_FOLDER, f"pozadie_vesmir_n{i}{ext}")
        if os.path.exists(path):
            image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (150, 90))
            break
    if image is None:
        image = pygame.Surface((180, 110))
    map_images.append(image)


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
button_width, button_height, border_radius = 250, 75, 7
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
    draw_gradient_button(screen, start_button,SPACE_BLUE, PURPLE, "START", font, WHITE)
    draw_gradient_button(screen, back_button,SPACE_BLUE, PURPLE, "BACK", font, WHITE)

    # Nadpisy
    text1 = custom_font.render("SETTINGS", True, WHITE)
    screen.blit(text1, text1.get_rect(center=(width // 2, 75)))

    text2 = custom_font.render("CHOOSE MAP", True, WHITE)
    screen.blit(text2, text2.get_rect(center=(width // 2, 150)))

    text3 = custom_font.render("CHOOSE CHARACTER", True, WHITE)
    screen.blit(text3, text3.get_rect(center=(width // 2, height // 2 + 70)))

    # Mapa a raketky
    for i, pos in enumerate(map_positions):
        color = YELLOW if selected_map == i else WHITE
        pygame.draw.rect(screen, color, (pos[0] - 5, pos[1] - 5, 160, 100), 5, border_radius=7)
        screen.blit(map_images[i], pos)

    for i, pos in enumerate(control_positions):
        color = YELLOW if selected_control == i else WHITE
        pygame.draw.rect(screen, color, (pos[0] - 5, pos[1] - 5, 170, 100), 5, border_radius=7)
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
