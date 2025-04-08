import subprocess
import sys

import pygame

# Inicializácia Pygame
pygame.init()

# Nastavenie veľkosti okna na celú obrazovku
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

# Farby a Font
WHITE = (255, 255, 255)
DARK_GRAY = (169, 169, 169)
SPACE_BLUE = (10, 10, 40)
font = pygame.font.Font(None, 50)

# Pozadie
screen.fill(SPACE_BLUE)

# Umiestnenie
button_width, button_height, border_radius = 250, 50, 20
start_button = pygame.Rect(SCREEN_WIDTH - button_width - 40, SCREEN_HEIGHT - button_height - 40, button_width, button_height)
back_button = pygame.Rect(40, SCREEN_HEIGHT - button_height - 40, button_width, button_height)

# Pozadie tlacidiel, zaoblenie
pygame.draw.rect(screen, DARK_GRAY, start_button, border_radius=border_radius)
pygame.draw.rect(screen, DARK_GRAY, back_button, border_radius=border_radius)

# Text tlacidiel, farba
start_text = font.render("START", True, WHITE)
exit_text = font.render("BACK", True, WHITE)

# Vycentrovanie textu
screen.blit(start_text, start_text.get_rect(center=start_button.center))
screen.blit(exit_text, exit_text.get_rect(center=back_button.center))

# NADPIS
title_text = font.render("NASTAVENIA HRY", True, WHITE)
screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))



# Hlavná Slučka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):     #Naspať do hlavnej obrazovky
                subprocess.run(["python","uvodne_okno.py"])
                pygame.quit()
                sys.exit()
            if start_button.collidepoint(event.pos):    #Tlačidlo na spustenie hry
                pass
    # Aktualizácia obrazovky
    pygame.display.update()

pygame.quit()
sys.exit()