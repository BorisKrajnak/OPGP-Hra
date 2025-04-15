import os
import subprocess
import sys
import pygame
import time

# Inicializácia Pygame
pygame.init()

# Nastavenie veľkosti okna na celú obrazovku
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Nastavenia hry")

# Farby
WHITE = (255, 255, 255)
DARK_GRAY = (169, 169, 169)
SPACE_BLUE = (10, 10, 40)
YELLOW = (255, 255, 0)

# Fonty
loading_font = pygame.font.SysFont("Arial", 60)
font = pygame.font.Font(None, 50)

# Settings
screen.fill(SPACE_BLUE)
loading_text = loading_font.render("Settings...", True, WHITE)
screen.blit(loading_text, (width // 2 - loading_text.get_width() // 2, height // 2))
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

# Rozloženie máp
map_positions = [
    (width // 2 - 540 + (i % 6) * 180, height // 2 - 240 + (i // 6) * 110) for i in range(12)
]

# Rozloženie raketiek
control_positions = [
    (width // 2 - 280, height // 2 + 120),
    (width // 2 - 80, height // 2 + 120),
    (width // 2 + 120, height // 2 + 120)
]

selected_map = None
selected_control = None

# Pozadie
screen.fill(SPACE_BLUE)

# Umiestnenie
button_width, button_height, border_radius = 250, 50, 20
start_button = pygame.Rect(width - button_width - 40, height - button_height - 40, button_width, button_height)
back_button = pygame.Rect(40, height - button_height - 40, button_width, button_height)

# Pozadie tlacidiel, zaoblenie
pygame.draw.rect(screen, DARK_GRAY, start_button, border_radius=border_radius)
pygame.draw.rect(screen, DARK_GRAY, back_button, border_radius=border_radius)

# Text tlacidiel, farba
start_text = font.render("START", True, WHITE)
back_text = font.render("BACK", True, WHITE)

# Vycentrovanie textu
screen.blit(start_text, start_text.get_rect(center=start_button.center))
screen.blit(back_text, back_text.get_rect(center=back_button.center))

# NADPIS NASTAVENIA HRY
title_text = font.render("NASTAVENIA HRY", True, WHITE)
screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))

#NADPIS VÝBER MAPY
map_selection_text = font.render("VÝBER MAPY:", True, WHITE)
screen.blit(map_selection_text, (width // 2 - map_selection_text.get_width() // 2, 110))

# Výber raketky
control_selection_text = font.render("VÝBER RAKETKY:", True, WHITE)
screen.blit(control_selection_text, (width // 2 - control_selection_text.get_width() // 2, height // 2 + 70))

# Hlavný cyklus
running = True
while running:
    #Zobrazenie máp
    for i, pos in enumerate(map_positions):
        color = YELLOW if selected_map == i else WHITE
        pygame.draw.rect(screen, color, (pos[0] - 5, pos[1] - 5, 160, 100), 5)
        screen.blit(map_images[i], pos)

    # Zobrazenie raketiek
    for i, pos in enumerate(control_positions):
        color = YELLOW if selected_control == i else WHITE
        pygame.draw.rect(screen, color, (pos[0] - 5, pos[1] - 5, 170, 100), 5)
        screen.blit(control_images[i], pos)

    #Udalosti
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):  # Naspať do hlavnej obrazovky
                subprocess.Popen(["python", "uvodne_okno.py"], creationflags=subprocess.CREATE_NO_WINDOW) # Toto potlačí okno príkazového riadku
                time.sleep(0.5)
                running = False
                pygame.quit()
                sys.exit()
            if start_button.collidepoint(event.pos):  # Tlačidlo na spustenie hry
                pass

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Výber mapy
            for i, pos in enumerate(map_positions):
                rect = pygame.Rect(pos[0], pos[1], 150, 90)
                if rect.collidepoint(event.pos):
                    selected_map = i
            #Výber raketky
            for i, pos in enumerate(control_positions):
                rect = pygame.Rect(pos[0], pos[1], 160, 90)
                if rect.collidepoint(event.pos):
                    selected_control = i

    #Aktualizácia obrazovky
    pygame.display.flip()

pygame.quit()
sys.exit()
