import pygame
import sys
import os

from vyber_pozadia import nacitaj_pozadie

# Inicializácia Pygame
pygame.init()

# Nastavenie rozlíšenia na celé okno
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Raketka")

# Načítanie pozadia cez import
background = nacitaj_pozadie("game_config.json",width,height)

# Parametre raketky
player_width, player_height = 120, 120
player_x, player_y = width // 2, height // 2
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

rotation_angle = 0

# Hlavný cyklus
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()
    # Pohyb raketky
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

    # Animácia
    if pygame.time.get_ticks() - last_frame_time > frame_rate:
        current_frame = (current_frame + 1) % len(player_frames)
        last_frame_time = pygame.time.get_ticks()

    # Kreslenie scény
    screen.blit(background, (0, 0))
    rotated_frame = pygame.transform.rotate(player_frames[current_frame], rotation_angle)
    frame_rect = rotated_frame.get_rect(center=(player_x, player_y))
    screen.blit(rotated_frame, frame_rect.topleft)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()