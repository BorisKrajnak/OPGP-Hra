import pygame
import sys

from vyber_pozadia import nacitaj_pozadie, nacitaj_obrazok

# Inicializácia Pygame
pygame.init()

# Nastavenie rozlíšenia na celé okno
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hra - UFO")

# Načítanie pozadia a obrázka prostreidku cez import
background = nacitaj_pozadie("game_config.json",width,height)
control_image, control_rect = nacitaj_obrazok("img/ovladanie/ovladanie2.png", width // 2, height // 2)

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
