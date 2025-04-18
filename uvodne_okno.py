import subprocess
import pygame
import sys
import time

# Inicializácia Pygame
pygame.init()

# Nastavenie veľkosti okna na celú obrazovku
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Vesmírna hra")  # Názov okna

#Farby
WHITE = (255, 255, 255)
SPACE_BLUE = (10, 10, 40)
DARK_GRAY = (169, 169, 169)

# Definovanie fontov pre text
font = pygame.font.SysFont("Arial", 40, bold=True)
small_font = pygame.font.SysFont("Arial", 28)
loading_font = pygame.font.SysFont("Arial", 60)

#Welcome
screen.fill(SPACE_BLUE)
welcome_text = loading_font.render("Welcome...", True, WHITE)
screen.blit(welcome_text, (width // 2 - welcome_text.get_width() // 2, height // 2))
pygame.display.update()
time.sleep(0.5)


# Načítanie obrázka pozadia
try:
    background_img = pygame.image.load(r"img/pozadie_uvodne_okno.jpg")
    background_img = pygame.transform.scale(background_img, (int(background_img.get_width()), int(background_img.get_height())))
except Exception as e:
    print(f"Chyba pri načítaní obrázka: {e}")
    background_img = None

# Parametre pre tlačidlá
button_width = 250
button_height = 50
border_radius = 20

# Nastavenie pozície tlačidiel
padding = 40
quit_button_rect = pygame.Rect(padding, height - button_height - padding, button_width, button_height)
rules_button_rect = pygame.Rect((width - button_width) // 2, height - button_height - padding, button_width, button_height)
next_button_rect = pygame.Rect(width - button_width - padding, height - button_height - padding, button_width, button_height)

# Text tlačidiel
quit_button_text = font.render("QUIT", True, WHITE)  # Tlačidlo "QUIT"
next_button_text = font.render("NEXT", True, WHITE)  # Tlačidlo "NEXT"
rules_button_text = font.render("RULES", True, WHITE)  # Tlačidlo "RULES"

# Určenie pozície textu v tlačidlách
quit_button_text_rect = quit_button_text.get_rect(center=quit_button_rect.center)
next_button_text_rect = next_button_text.get_rect(center=next_button_rect.center)
rules_button_text_rect = rules_button_text.get_rect(center=rules_button_rect.center)

# Nadpis (názov hry)
title_text = font.render("SPACE RIDER", True, WHITE)

# Premenná na sledovanie, či sú pravidlá zobrazené
showing_rules = False

# Funkcia na vykreslenie okna s pravidlami
def draw_rules_popup():
    # Definovanie veľkosti okna pre pravidlá
    popup_width, popup_height = 800, 700
    popup_surface = pygame.Surface((popup_width, popup_height))  # Vytvorenie povrchu pre pravidlá
    popup_surface.fill((30, 30, 30))  # Nastavenie pozadia na tmavú farbu
    pygame.draw.rect(popup_surface, WHITE, popup_surface.get_rect(), 3)  # Rám okolo pravidiel

    heading = "PRAVIDLÁ HRY"  # Nadpis pre pravidlá
    heading_surface = font.render(heading, True, WHITE)
    popup_surface.blit(heading_surface, ((popup_width - heading_surface.get_width()) // 2, 20))  # Zarovnanie nadpisu na stred

    # Text pravidiel
    rules_lines = [
        "",
        "- Cieľom je prežiť čo najdlhšie vo vesmíre a získať maximálne skóre.",
        "- Na ďalšej obrazovke si vyberáš 1 z 11 máp – alebo to necháš na náhodu.",
        "- Vyber si svoj lietajúci stroj – raketku, UFO alebo Omnimana.",
        "- Každý má jedinečný štýl ovládania – zvládneš ich všetky?",
        "- V ceste ti budú stáť prekážky, nepriatelia a vesmírne pasce.",
        "- Zbieraj body, palivo a power-upy pre lepšiu šancu na prežitie.",
        "- Hra končí, keď narazíš, stratíš životy alebo palivo.",
        "- Niektoré power-upy sú dočasné – využi ich múdro.",
        "- Ovládanie: WASD alebo gamepad (ak je pripojený) :D :D :D"
    ]

    # Zobrazenie pravidiel jeden po druhom
    for i, line in enumerate(rules_lines):
        text = small_font.render(line, True, WHITE)  # Vytvorenie textu pravidla
        popup_surface.blit(text, (30, 80 + i * 45))  # Zobrazenie textu na obrazovke

    # Zobrazenie okna s pravidlami na obrazovke
    popup_rect = popup_surface.get_rect(center=(width // 2, height // 2))  # Pozícia okna s pravidlami na obrazovke
    screen.blit(popup_surface, popup_rect)  # Zobrazenie pravidiel

# Hlavná slučka hry
running = True
while running:
    # Skenovanie udalostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Ukončí hru, ak sa zavrie okno
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # Ukončí hru, ak sa stlačí ESC
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button_rect.collidepoint(event.pos):  # Ak klikneš na "QUIT"
                running = False
            elif next_button_rect.collidepoint(event.pos):  # Ak klikneš na "NEXT"
                subprocess.Popen(["python", "nastavenia_hry.py"], creationflags=subprocess.CREATE_NO_WINDOW) # Toto potlačí okno príkazového riadku
                time.sleep(0.5)
                running = False
                pygame.quit()
                sys.exit()
            elif rules_button_rect.collidepoint(event.pos):  # Ak klikneš na "RULES"
                showing_rules = not showing_rules  # Toggle (prepínač) pre zobrazenie/skrytie pravidiel

    # Vykreslenie pozadia hry
    if background_img:
        screen.blit(background_img, ((width - background_img.get_width()) // 2, (height - background_img.get_height()) // 4))  # Ak existuje obrázok, vykreslí ho
    else:
        screen.fill((0, 0, 0))  # Ak nie, vyplní obrazovku čiernou farbou

    # Vykreslenie tlačidiel na obrazovke
    pygame.draw.rect(screen, DARK_GRAY, quit_button_rect, border_radius=border_radius)
    pygame.draw.rect(screen, DARK_GRAY, next_button_rect, border_radius=border_radius)
    pygame.draw.rect(screen, DARK_GRAY, rules_button_rect, border_radius=border_radius)

    # Zobrazenie textu na tlačidlách
    screen.blit(quit_button_text, quit_button_text_rect)
    screen.blit(next_button_text, next_button_text_rect)
    screen.blit(rules_button_text, rules_button_text_rect)

    # Zobrazenie nadpisu
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))  # Názov hry

    # Zobrazenie pravidiel, ak sú zvolené
    if showing_rules:
        draw_rules_popup()

    # Aktualizácia obrazovky
    pygame.display.update()  # Prekreslí obrazovku s novými prvkami

# Ukončenie Pygame
pygame.quit()
sys.exit()
