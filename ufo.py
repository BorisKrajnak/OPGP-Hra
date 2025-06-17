# --- Načítanie knižníc ---
import json
import pygame
import sys
import os
import random
import subprocess
import time
from music_manager import toggle_music, set_volume, get_music_state, start_music, toggle_mute

from vyber_pozadia import nacitaj_pozadie

from music_manager import start_music
start_music()

# --- Funkcie na uloženie konfigurácie a skóre ---

# Uloží názov aktuálne aktívnej hry do konfiguračného súboru
def save_game_config(game_name):
    if not os.path.exists("game_config.json"):
        config = {"active_game": game_name}
        with open("game_config.json", "w") as f:
            json.dump(config, f, indent=4)
    else:
        with open("game_config.json", "r") as f:
            config = json.load(f)
        config["active_game"] = game_name
        with open("game_config.json", "w") as f:
            json.dump(config, f, indent=4)

# Uloží skóre a čas do súboru skore.json
def save_score(score, elapsed_time):
    data = {"skore": score, "cas": int(elapsed_time)}
    with open("skore.json", "w") as f:
        json.dump(data, f, indent=4)

# Porovná aktuálne skóre s najlepším a ak je vyššie, uloží ho
def uloz_best_score(score):
    try:
        with open("best_score_ufo.json", "r") as f:
            data = json.load(f)
            best = data.get("best", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        best = 0

    if score > best:
        with open("best_score_ufo.json", "w") as f:
            json.dump({"best": score}, f)

# --- Inicializácia Pygame a okna ---
pygame.init()
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("UFO")

# Farby
WHITE = (255, 255, 255)
PURPLE = (31, 10, 30)
DARK_GRAY = (50, 50, 50)

# Tlačidlo pre hudbu (v pravom hornom rohu)
music_button_size = 60
music_button_rect = pygame.Rect(width - music_button_size - 20, 20, music_button_size, music_button_size)

# --- Načítanie pozadia ---
background = nacitaj_pozadie("game_config.json", width, height)
loaded_images = {}

# Funkcia na načítanie animovaných snímok UFO
def nacitaj_animaciu(cesta, x, y, scale=0.25):
    frames = []
    for filename in sorted(os.listdir(cesta)):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            if filename not in loaded_images:
                image = pygame.image.load(os.path.join(cesta, filename)).convert_alpha()
                new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
                image = pygame.transform.scale(image, new_size)
                loaded_images[filename] = image
            rect = loaded_images[filename].get_rect(center=(x, y))
            frames.append((loaded_images[filename], rect))
    return frames

# --- HUD obrázky ---
star_img = pygame.image.load(r"img/doplnky/star.png").convert_alpha()
star_img = pygame.transform.scale(star_img, (45, 45))

time_img = pygame.image.load(r"img/doplnky/time.png").convert_alpha()
time_img = pygame.transform.scale(time_img, (45, 45))

font_path = "Font/VOYAGER.ttf"
font = pygame.font.Font(font_path, 40)

# --- UFO nastavenia ---
ufo_x = width // 2
ufo_y = height // 2
ufo_speed = 0
gravity = 0.5
jump_strength = -10
move_speed = 5
ufo_frames = nacitaj_animaciu("img/ufo_frames", ufo_x, ufo_y)
image, _ = ufo_frames[0]
ufo_width, ufo_height = image.get_width(), image.get_height()

# --- Palivo ---
max_fuel = 100
fuel = max_fuel
fuel_depletion_rate = 0.2
last_fuel_update = pygame.time.get_ticks()

barrel_image = pygame.image.load(r"img/palivo/barrel_ufo.png").convert_alpha()
barrel_spawn_interval = 10000
last_barrel_spawn = pygame.time.get_ticks()
barrels = []

# Objekt paliva (barrel), ktorý UFO môže zbierať
class Barrel:
    def __init__(self):
        self.size = 30
        self.image = pygame.transform.scale(barrel_image, (self.size, self.size))
        self.x = width + self.size
        self.y = random.randint(0, height - self.size)
        self.speed = random.uniform(3.0, 6.0)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.x -= self.speed
        self.rect.x = int(self.x)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.x < -self.size

# --- Meteory ako prekážky ---
meteor_image = pygame.image.load(os.path.join("img", "prekazky", "meteor2.png")).convert_alpha()

class Meteor:
    def __init__(self, speed_multiplier):
        self.size = random.randint(40, 100)
        original = pygame.transform.scale(meteor_image, (self.size, self.size))
        self.image = pygame.transform.rotate(original, -45)
        self.x = width + self.image.get_width()
        self.y = random.randint(0, height - self.image.get_height())
        self.speed = random.uniform(6.0, 12.0) * speed_multiplier
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.x -= self.speed
        self.rect.x = int(self.x)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.x + self.image.get_width() < 0

# --- Nastavenie animácie a spawnu ---
frame_index = 0
frame_delay = 70
last_update = pygame.time.get_ticks()

meteory = []
spawn_delay = 500
last_spawn_time = pygame.time.get_ticks()

# --- Hlavný cyklus ---
clock = pygame.time.Clock()
running = True

save_game_config("ufo")
meteory_prelietane = 0
start_time = pygame.time.get_ticks()

# Načítanie najlepšieho skóre
try:
    with open("best_score_ufo.json", "r") as f:
        best_data = json.load(f)
        best_score = best_data.get("best", 0)
except:
    best_score = 0

while running:
    screen.blit(background, (0, 0))

    # --- Ovládanie a udalosť ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            ufo_speed = jump_strength
        if event.type == pygame.MOUSEBUTTONDOWN and music_button_rect.collidepoint(event.pos):  # Ovládanie hudby
            # Pri kliknutí pravým tlačidlom - nastavenie štandardnej hlasitosti
            if event.button == 3:  # Pravé tlačidlo myši
                # Nastavenie štandardnej hlasitosti (0.5)
                set_volume(0.5)
                MUSIC_STATE = get_music_state()
                MUSIC_STATE["muted"] = False
            # Pri kliknutí ľavým tlačidlom - stlmenie/obnovenie
            else:
                toggle_mute()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        ufo_x -= move_speed
    if keys[pygame.K_d]:
        ufo_x += move_speed

    # --- Fyzika pohybu UFO ---
    ufo_speed += gravity
    ufo_y += ufo_speed
    ufo_x = max(0, min(ufo_x, width - ufo_width))
    ufo_y = max(0, min(ufo_y, height - ufo_height))
    if ufo_y == height - ufo_height:
        ufo_speed = 0

    # --- Výpočet skóre ---
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000
    current_score = meteory_prelietane + elapsed_time

    # --- Palivo ubúda v čase ---
    if current_time - last_fuel_update > 100:
        fuel -= fuel_depletion_rate
        last_fuel_update = current_time
        if fuel <= 0:
            save_score(current_score, elapsed_time)
            uloz_best_score(current_score)
            subprocess.Popen(["python", "game_over.py"], creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(0.5)
            pygame.quit()
            sys.exit()

    # --- Animácia UFO ---
    if current_time - last_update > frame_delay:
        frame_index = (frame_index + 1) % len(ufo_frames)
        last_update = current_time

    current_ufo_image = ufo_frames[frame_index][0]
    screen.blit(current_ufo_image, (ufo_x, ufo_y))
    ufo_rect = current_ufo_image.get_rect(topleft=(ufo_x, ufo_y))
    ufo_mask = pygame.mask.from_surface(current_ufo_image)

    # Vykreslenie tlačidla pre hudbu
    music_state = get_music_state()
    music_color = PURPLE if not music_state["muted"] else DARK_GRAY
    pygame.draw.circle(screen, music_color, music_button_rect.center, music_button_size // 2)
    pygame.draw.circle(screen, WHITE, music_button_rect.center, music_button_size // 2, 2)  # Obrys

    # Ikona hudby v tlačidle - dve paličky
    bar_width = 5
    bar_height = music_button_size // 3
    spacing = 10
    center_x = music_button_rect.centerx
    center_y = music_button_rect.centery

    # Prvá palička
    left_bar_x = center_x - spacing // 2 - bar_width
    pygame.draw.rect(screen, WHITE, (left_bar_x, center_y - bar_height // 2, bar_width, bar_height))

    # Druhá palička
    right_bar_x = center_x + spacing // 2
    pygame.draw.rect(screen, WHITE, (right_bar_x, center_y - bar_height // 2, bar_width, bar_height))

    # Indikátor stlmenia - ak je stlmené, prekrížiť paličky
    if music_state["muted"]:
        slash_length = music_button_size // 3
        slash_width = 3
        # Diagonálna čiara cez ikonu
        pygame.draw.line(screen, WHITE,
                        (center_x - slash_length, center_y - slash_length),
                        (center_x + slash_length, center_y + slash_length), slash_width)

    # --- Spawn meteorov podľa obtiažnosti ---
    speed_multiplier = 1.0 + (elapsed_time // 30) * 0.2
    if current_time - last_spawn_time > max(300, spawn_delay - (elapsed_time * 10)):
        meteory.append(Meteor(speed_multiplier))
        last_spawn_time = current_time

    for meteor in meteory[:]:
        meteor.update()
        if meteor.is_off_screen():
            meteory.remove(meteor)
            meteory_prelietane += 1
            continue
        offset = (int(meteor.x - ufo_rect.left), int(meteor.y - ufo_rect.top))
        if ufo_mask.overlap(meteor.mask, offset):
            save_score(current_score, elapsed_time)
            uloz_best_score(current_score)
            subprocess.Popen(["python", "game_over.py"], creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(0.5)
            pygame.quit()
            sys.exit()
        meteor.draw(screen)

    # --- Spawn paliva ---
    if current_time - last_barrel_spawn > barrel_spawn_interval:
        barrels.append(Barrel())
        last_barrel_spawn = current_time

    for barrel in barrels[:]:
        barrel.update()
        if barrel.is_off_screen():
            barrels.remove(barrel)
            continue
        offset = (int(barrel.x - ufo_rect.left), int(barrel.y - ufo_rect.top))
        if ufo_mask.overlap(barrel.mask, offset):
            fuel = min(max_fuel, fuel + 15)
            barrels.remove(barrel)
            continue
        barrel.draw(screen)

    # --- HUD vykreslenie ---
    hud_x = 10
    hud_y = 10
    line_height = 55

    screen.blit(star_img, (hud_x, hud_y))
    score_text = font.render(f"SCORE: {current_score}", True, (255, 255, 255))
    screen.blit(score_text, (hud_x + 50, hud_y + 5))

    screen.blit(time_img, (hud_x, hud_y + line_height))
    time_text = font.render(f"TIME: {elapsed_time}s", True, (255, 255, 255))
    screen.blit(time_text, (hud_x + 50, hud_y + line_height + 5))

    fuel_ratio = fuel / max_fuel
    bar_top = hud_y + 2 * line_height + 5
    pygame.draw.rect(screen, (0, 0, 0), (hud_x, bar_top, 234, 44))
    pygame.draw.rect(screen, (30, 30, 30), (hud_x + 4, bar_top + 4, 226, 36))
    pygame.draw.rect(screen, (60, 60, 60), (hud_x + 8, bar_top + 8, 218, 28))
    pygame.draw.rect(screen, (0, 0, 0), (hud_x + 10, bar_top + 10, 214, 24))
    pygame.draw.rect(
        screen,
        (0, 255, 0) if fuel_ratio >= 0.65 else (255, 165, 0) if fuel_ratio >= 0.25 else (255, 0, 0),
        (hud_x + 10, bar_top + 10, int(214 * fuel_ratio), 24)
    )

    pygame.display.flip()
    clock.tick(60)

# --- Ukončenie ---
pygame.quit()
sys.exit()
