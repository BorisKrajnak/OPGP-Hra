import pygame
import sys
import os

from vyber_pozadia import nacitaj_pozadie

# Inicializácia Pygame
pygame.init()

# Nastavenie rozlíšenia na celé okno
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("UFO")

# Parametre UFO
ufo_x = width // 2
ufo_y = height // 2
ufo_speed = 0
gravity = 0.5
jump_strength = -10
move_speed = 5

# Načítanie pozadia z konfiguračného súboru
background = nacitaj_pozadie("game_config.json", width, height)

# Slovník pre uloženie načítaných obrázkov, aby sa načítali len raz
loaded_images = {}

# Funkcia na načítanie a zmenšenie všetkých obrázkov z priečinka ako animáciu
def nacitaj_animaciu(cesta, x, y, scale=0.25):
    frames = []
    for filename in sorted(os.listdir(cesta)):  # Prechádza všetky obrázky v priečinku
        if filename.endswith((".png", ".jpg", ".jpeg")):
            # Ak obrázok ešte nebol načítaný, načíta ho a upraví veľkosť
            if filename not in loaded_images:
                image = pygame.image.load(os.path.join(cesta, filename)).convert_alpha()
                new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
                image = pygame.transform.scale(image, new_size)
                loaded_images[filename] = image
            rect = image.get_rect(center=(x, y))  # Nastaví pozíciu obrázku
            frames.append((image, rect))  # Pridá obrázok a jeho rect do zoznamu
    return frames

# Načítanie animácie z priečinka ufo_frames
ufo_frames = nacitaj_animaciu("img/ufo_frames", ufo_x, ufo_y)

# Premenné pre animáciu
frame_index = 0
frame_delay = 70  # Čas medzi rámčekmi v milisekundách
last_update = pygame.time.get_ticks()

# Zistenie rozmerov UFO na základe prvého rámčeka
image, _ = ufo_frames[0]
ufo_width, ufo_height = image.get_width(), image.get_height()

# Hlavná slučka hry – beží dovtedy, kým je `running` True
running = True
clock = pygame.time.Clock()
while running:
    screen.blit(background, (0, 0))  # Vykreslí pozadie na obrazovku

    # Spracovanie udalostí (zatvorenie okna, stlačenie kláves)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False  # Ukončenie hry
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                ufo_speed = jump_strength  # Skok UFO pri stlačení W

    # Detekcia stlačených klávesov pre pohyb doľava alebo doprava
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        ufo_x -= move_speed  # Pohyb doľava
    elif keys[pygame.K_d]:
        ufo_x += move_speed  # Pohyb doprava

    # Aplikovanie gravitácie a pohyb UFO po y-osi
    ufo_speed += gravity
    ufo_y += ufo_speed

    # Obmedzenie UFO v rámci obrazovky
    ufo_x = max(0, min(ufo_x, width - ufo_width))
    ufo_y = max(0, min(ufo_y, height - ufo_height))
    if ufo_y == height - ufo_height:
        ufo_speed = 0  # Nulovanie rýchlosti po dopade na spodok

    # Animácia UFO – výmena rámčekov podľa časového oneskorenia
    current_time = pygame.time.get_ticks()
    if current_time - last_update > frame_delay:
        frame_index = (frame_index + 1) % len(ufo_frames)
        last_update = current_time

    # Vykreslenie aktuálneho rámčeka animácie UFO
    screen.blit(ufo_frames[frame_index][0], (ufo_x, ufo_y))

    pygame.display.flip()
    clock.tick(60)

# Ukončenie Pygame a skriptu
pygame.quit()
sys.exit()
