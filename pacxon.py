import pygame
import tilemap
import control
import tilemap_view
import tilemap_objects
import stats

clock = pygame.time.Clock() #tworzy obiekt, ktory pozwala sledzic czas
pygame.init() #inicjuje zaimportowane moduły pygame
pygame.display.set_caption('PACXON') #ustawia naglowek okna

control.start_game() #ekran startowy i rozpoczecie wybranego levelu

while not control.done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            control.done = True

    tilemap_view.draw() #narysuj nowy level 

    tilemap_objects.action() 

    pygame.display.flip()
    clock.tick(60)
