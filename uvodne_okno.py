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
    background_img = pygame.image.load(r"pozadie_uvodne_okno.jpg")
    background_img = pygame.transform.scale(background_img, (int(background_img.get_width() * 0.8), int(background_img.get_height() * 0.8)))
    screen.blit(background_img, ((width - background_img.get_width()) // 2, (height - background_img.get_height()) // 4))
except Exception as e:
    print(f"Chyba pri načítaní obrázka: {e}")

# Tlačidlo ukončiť
button_width = 250
button_height = 50
border_radius = 20

quit_button_rect = pygame.Rect(40, height - button_height - 40, button_width, button_height)
button_color = (169,169,169) # Sivá
pygame.draw.rect(screen, button_color, quit_button_rect, border_radius = border_radius)# Zaoblene rohy

# Nastavenie fontu a bilej farby tetxu
font = pygame.font.SysFont("Arial", 40, bold=True)
quit_button_text = font.render("UKONČIŤ", True, (255,255,255))

#Zarovnanie tlačidla na stred
quit_button_text_rect = quit_button_text.get_rect(center = quit_button_rect.center)
screen.blit(quit_button_text, quit_button_text_rect)


# Hlavná slučka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Ukončujem hru")
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Ukončenie pomocou klávesy ESC
                print("Ukončujem hru")
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button_rect.collidepoint(event.pos): # Ukončenie pomocou tlačidla
                print("Ukončujem hru")
                running = False


    # Aktualizácia obrazovky
    pygame.display.update()

# Ukončenie Pygame
pygame.quit()
sys.exit()
