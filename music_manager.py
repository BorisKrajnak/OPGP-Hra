import pygame

pygame.mixer.init()

def start_music():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('music/music_02.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
