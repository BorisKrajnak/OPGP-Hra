import json
import pygame
import sys
import os
import random
import subprocess
import time

from vyber_pozadia import nacitaj_pozadie


from music_manager import start_music
start_music()


# Funkcia na uloženie aktívnej hry do JSON
def save_game_config(game_name):
    # Skontroluj, či súbor existuje
    if not os.path.exists("game_config.json"):
        # Ak neexistuje, vytvor nový súbor s default hodnotou
        config = {"active_game": game_name}
        with open("game_config.json", "w") as f:
            json.dump(config, f, indent=4)
    else:
        # Ak súbor existuje, načítaj aktuálne nastavenia a uprav hodnotu
        with open("game_config.json", "r") as f:
            config = json.load(f)

        config["active_game"] = game_name  # Uprav hodnotu aktívnej hry

        # Ulož upravený config späť do súboru
        with open("game_config.json", "w") as f:
            json.dump(config, f, indent=4)


def uloz_best_score(score):
    try:
        with open("best_score_raketka.json", "r") as f:
            data = json.load(f)
            best = data.get("best", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        best = 0

    if score > best:
        with open("best_score_raketka.json", "w") as f:
            json.dump({"best": score}, f)


# Inicializácia Pygame
pygame.init()

# Nastavenie rozlíšenia na celé okno
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Raketka")
clock = pygame.time.Clock()

# Načítanie pozadia
background = nacitaj_pozadie("game_config.json", width, height)

# Parametre raketky
player_width, player_height = 120, 120
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

# Načítanie obrázka meteoritu
meteor_image = pygame.image.load(os.path.join("img", "prekazky", "meteor.png")).convert_alpha()

# Trieda Meteor
class Meteor:
    def __init__(self):
        self.size = random.randint(40, 100)
        self.image = pygame.transform.scale(meteor_image, (self.size, self.size))
        self.x = width + self.size
        self.y = random.randint(0, height - self.size)
        self.speed = random.uniform(3.0, 8.0)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.x -= self.speed
        self.rect.x = int(self.x)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.x + self.size < 0

# Hlavná hra
def spusti_hru():
    global current_frame, last_frame_time

    player_x, player_y = width // 2, height // 2
    current_frame = 0
    last_frame_time = pygame.time.get_ticks()

    meteory = []
    spawn_delay = 1200
    last_spawn_time = pygame.time.get_ticks()
    running = True

    start_time = pygame.time.get_ticks()

    font_path = "Font/VOYAGER.ttf"
    font = pygame.font.Font(font_path, 50)

    # --- HUD obrázky ---
    star_img = pygame.image.load(r"img/doplnky/star.png").convert_alpha()
    star_img = pygame.transform.scale(star_img, (45, 45))

    time_img = pygame.image.load(r"img/doplnky/time.png").convert_alpha()
    time_img = pygame.transform.scale(time_img, (45, 45))

    base_speed = 3.0
    max_speed = 12.0
    min_spawn_delay = 400
    meteory_velkost_min = 40
    meteory_velkost_max = 100
    meteory_obehol = 0

    fuel = 100
    fuel_depletion_rate = 0.04
    fuel_bar_position = (20, 120)
    fuel_bar_size = (300, 25)

    fuel_spawn_time = 0
    fuel_duration = 5000
    fuel_pos = None
    fuel_size = 60

    fuel_image = pygame.image.load(os.path.join("img", "palivo", "fuel.png")).convert_alpha()
    fuel_image = pygame.transform.scale(fuel_image, (fuel_size, fuel_size))
    fuel_mask = pygame.mask.from_surface(fuel_image)

    def spawn_fuel():
        x = random.randint(fuel_size, width - fuel_size)
        y = random.randint(fuel_size, height - fuel_size)
        return (x, y)

    # Hlavný cyklus
    while running:
        screen.blit(background, (0, 0))

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        score = meteory_obehol + elapsed_time

        hud_x = 10
        hud_y = 10
        line_height = 55

        screen.blit(star_img, (hud_x, hud_y))
        score_surface = font.render(f"SCORE: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (hud_x + 50, hud_y + 5))

        screen.blit(time_img, (hud_x, hud_y + line_height))
        time_surface = font.render(f"TIME: {elapsed_time}s", True, (255, 255, 255))
        screen.blit(time_surface, (hud_x + 50, hud_y + line_height + 5))

        if elapsed_time % 5 == 0:
            base_speed = min(base_speed + 0.1, max_speed)
            spawn_delay = max(spawn_delay - 10, min_spawn_delay)
            meteory_velkost_max = min(meteory_velkost_max + 1, 160)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        rotation_angle = 0
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

        # Animácia raketky
        if pygame.time.get_ticks() - last_frame_time > frame_rate:
            current_frame = (current_frame + 1) % len(player_frames)
            last_frame_time = pygame.time.get_ticks()

        # Spawn meteorov
        if pygame.time.get_ticks() - last_spawn_time > spawn_delay:
            meteorit = Meteor()
            meteorit.size = random.randint(meteory_velkost_min, meteory_velkost_max)
            meteorit.image = pygame.transform.scale(meteor_image, (meteorit.size, meteorit.size))
            meteorit.x = width + meteorit.size
            meteorit.y = random.randint(0, height - meteorit.size)
            meteorit.speed = random.uniform(base_speed, base_speed + 5.0)
            meteorit.rect = pygame.Rect(meteorit.x, meteorit.y, meteorit.size, meteorit.size)
            meteorit.mask = pygame.mask.from_surface(meteorit.image)
            meteory.append(meteorit)
            last_spawn_time = pygame.time.get_ticks()

        # Kreslenie scény
        rotated_frame = pygame.transform.rotate(player_frames[current_frame], rotation_angle)
        frame_rect = rotated_frame.get_rect(center=(player_x, player_y))
        player_mask = pygame.mask.from_surface(rotated_frame)

        # --- Fuel mechanics ---
        fuel -= fuel_depletion_rate
        fuel = max(fuel, 0)
        if fuel == 0:
            final_score = meteory_obehol + elapsed_time
            with open("skore.json", "w") as f:
                json.dump({"skore": final_score, "cas": elapsed_time}, f)
            uloz_best_score(score)
            subprocess.Popen(["python", "game_over.py"], creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(0.5)
            running = False
            pygame.quit()
            sys.exit()

        current_time = pygame.time.get_ticks()
        if fuel_pos is None and current_time - fuel_spawn_time > 15000:
            fuel_pos = spawn_fuel()
            fuel_spawn_time = current_time
        elif fuel_pos is not None and current_time - fuel_spawn_time > fuel_duration:
            fuel_pos = None

        # Zobraz palivo a kontroluj kolíziu podľa masky (presný hitbox)
        if fuel_pos is not None:
            screen.blit(fuel_image, fuel_pos)
            fuel_rect = pygame.Rect(fuel_pos[0], fuel_pos[1], fuel_size, fuel_size)
            offset = (fuel_rect.left - frame_rect.left, fuel_rect.top - frame_rect.top)
            if player_mask.overlap(fuel_mask, offset):
                fuel = min(fuel + 30, 100)
                fuel_pos = None

        for meteor in meteory[:]:
            meteor.update()
            if meteor.is_off_screen():
                meteory.remove(meteor)
                meteory_obehol += 1
                continue

            offset = (int(meteor.x - frame_rect.left), int(meteor.y - frame_rect.top))
            if player_mask.overlap(meteor.mask, offset):
                final_score = meteory_obehol + elapsed_time
                with open("skore.json", "w") as f:
                    json.dump({"skore": final_score, "cas": elapsed_time}, f)

                uloz_best_score(score)
                subprocess.Popen(["python", "game_over.py"],
                                 creationflags=subprocess.CREATE_NO_WINDOW)  # Toto potlačí okno príkazového riadku
                time.sleep(0.5)
                running = False
                pygame.quit()
                sys.exit()

            meteor.draw(screen)

        # Kreslenie raketky
        screen.blit(rotated_frame, frame_rect.topleft)

        # Draw fuel bar
        if fuel > 60:
            fuel_color = (0, 255, 0)
        elif fuel > 30:
            fuel_color = (255, 165, 0)
        else:
            fuel_color = (255, 0, 0)

        pygame.draw.rect(screen, (50, 50, 50), (*fuel_bar_position, *fuel_bar_size))
        filled_width = int(fuel_bar_size[0] * (fuel / 100))
        pygame.draw.rect(screen, fuel_color,
                         (fuel_bar_position[0], fuel_bar_position[1], filled_width, fuel_bar_size[1]))
        pygame.draw.rect(screen, (255, 255, 255), (*fuel_bar_position, *fuel_bar_size), 2)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    save_game_config("raketka")
    spusti_hru()
