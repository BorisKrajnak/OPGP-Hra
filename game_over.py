import json
import pygame
import subprocess
import sys
import time


# Funkcia na načítanie aktívnej hry z JSON
def load_game_config():
    try:
        with open("game_config.json", "r") as f:
            config = json.load(f)
            return config.get("active_game", "unknown")
    except FileNotFoundError:
        return "unknown"

pygame.init()
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Over")

# Farby
WHITE = (255, 255, 255)
SPACE_BLUE = (10, 10, 40)
DARK_GRAY = (169, 169, 169)
PURPLE = (31, 10, 30)

# Funkcia na gradiet
def draw_vertical_gradient(surface, top_color, bottom_color):
    for y in range(surface.get_height()):
        ratio = y / surface.get_height()
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

# Fonty
font_path = "Font/VOYAGER.ttf"
font = pygame.font.Font(font_path, 80)
button_font = pygame.font.Font(font_path, 50)
loading_font = pygame.font.Font(font_path, 200)

# Načítanie aktívnej hry
active_game = load_game_config()

# YOU LOSE
draw_vertical_gradient(screen, SPACE_BLUE, PURPLE)
welcome_text = loading_font.render("YOU LOSE", True, WHITE)
screen.blit(welcome_text, (
    width // 2 - welcome_text.get_width() // 2,
    height // 2 - welcome_text.get_height() // 2
))
pygame.display.update()
time.sleep(0.5)

# Funkcia na gradient button
def draw_gradient_button(rect, color1, color2, text):
    button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    for y in range(rect.height):
        ratio = y / rect.height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(button_surf, (r, g, b), (0, y), (rect.width, y))

    pygame.draw.rect(button_surf, WHITE, button_surf.get_rect(), 3, border_radius=10)
    screen.blit(button_surf, (rect.x, rect.y))

    text_surf = button_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

running = True
while running:
    draw_vertical_gradient(screen, SPACE_BLUE, PURPLE)

    # Nadpis
    game_over_text = font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, game_over_text.get_rect(center=(width // 2, height // 3)))

    # Tlačidlá
    btn_width, btn_height = 300, 70
    restart_button = pygame.Rect(width // 2 - 150, height // 2, btn_width, btn_height)
    settings_button = pygame.Rect(width // 2 - 150, height // 2 + 200, btn_width, btn_height)
    quit_button = pygame.Rect(width // 2 - 150, height // 2 + 100, btn_width, btn_height)

    draw_gradient_button(restart_button, SPACE_BLUE, PURPLE, "RESTART")
    draw_gradient_button(settings_button, SPACE_BLUE, PURPLE, "SETTINGS")
    draw_gradient_button(quit_button, SPACE_BLUE, PURPLE, "QUIT")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                if active_game != "unknown":
                    subprocess.Popen(["python", f"{active_game}.py"], creationflags=subprocess.CREATE_NO_WINDOW)
                    time.sleep(0.5)
                    pygame.quit()
                    sys.exit()
            if quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            if settings_button.collidepoint(event.pos):
                subprocess.Popen(["python", "nastavenia_hry.py"], creationflags=subprocess.CREATE_NO_WINDOW)
                time.sleep(0.5)
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r:
                if active_game != "unknown":
                    subprocess.Popen(["python", f"{active_game}.py"], creationflags=subprocess.CREATE_NO_WINDOW)
                    time.sleep(0.5)
                    pygame.quit()
                    sys.exit()

    pygame.display.flip()

pygame.quit()
