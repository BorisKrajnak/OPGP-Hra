import subprocess
import pygame
import sys

# Inicializácia Pygame
pygame.init()

# Nastavenie veľkosti okna na celú obrazovku
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()  # Získame veľkosť obrazovky
pygame.display.set_caption("Vesmírna hra")

# Načítanie obrázka
try:
    background_img = pygame.image.load(r"img/pozadie_uvodne_okno.jpg")
    background_img = pygame.transform.scale(background_img, (int(background_img.get_width()), int(background_img.get_height())))
    screen.blit(background_img, ((width - background_img.get_width()) // 2, (height - background_img.get_height()) // 4))
except Exception as e:
    print(f"Chyba pri načítaní obrázka: {e}")

# TLACIDLA
button_width = 250
button_height = 50
border_radius = 20

button_color = (169,169,169) # Sivá
font = pygame.font.SysFont("Arial", 40, bold=True) #Font

#Umiestnenie
quit_button_rect = pygame.Rect(40, height - button_height - 40, button_width, button_height)
next_button_rect = pygame.Rect(width - button_width - 40, height - button_height - 40, button_width, button_height)

#Pozadie tlacidiel, zaoblenie
pygame.draw.rect(screen, button_color, quit_button_rect, border_radius = border_radius)
pygame.draw.rect(screen, button_color, next_button_rect, border_radius=border_radius)

#Text tlacidiel, farba
quit_button_text = font.render("QUIT", True, (255,255,255))
next_button_text = font.render("NEXT", True, (255, 255, 255))

#Vycentrovanie textu
quit_button_text_rect = quit_button_text.get_rect(center = quit_button_rect.center)
start_button_text_rect = next_button_text.get_rect(center=next_button_rect.center)

screen.blit(quit_button_text, quit_button_text_rect)
screen.blit(next_button_text, start_button_text_rect)


#NADPIS
title_text = font.render("SPACE RIDER", True, (255, 255, 255))
screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))


# Hlavná slučka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Ukončenie pomocou klávesy ESC
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button_rect.collidepoint(event.pos): # Ukončenie pomocou tlačidla
                running = False
            if next_button_rect.collidepoint(event.pos): # Tlačidlo Next
                running = False
                pygame.quit()
                subprocess.run(["python","nastavenia_hry.py"])
                sys.exit()



    # Aktualizácia obrazovky
    pygame.display.update()

# Ukončenie Pygame
pygame.quit()
sys.exit()
