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



# Hlavná slučka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Aktualizácia obrazovky
    pygame.display.update()

# Ukončenie Pygame
pygame.quit()
sys.exit()
