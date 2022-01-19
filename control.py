import pygame
import tilemap_view
import time
import stats
import time
import tilemap
import tilemap_objects


done = False
f = "default_tile_map.txt"
gameover=False

def level_up():
    stats.this_level += 1
    stats.load_from_file()

def wait_for_keypress():
    wait = True
    time.sleep(.5)
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                wait = False
            if event.type == pygame.KEYDOWN:
                return


def game_over():
    global done
    done=True
    tilemap_view.game_over_view()
    tilemap_view.clear()
    done=False
    wait_for_keypress()
    


def win():
    global done
    done=True
    level_up()
    tilemap_view.game_win_view()
    tilemap_view.clear()
    done=False
    wait_for_keypress()

def start_game():
    tilemap.init_from_file("level1.txt")  #stworz tablice i okno (szerokosc, dlugosc)

    start_level = tilemap_view.start_view()  #tworzy widok startowy    

    stats.load_from_file(level=start_level) #ładuje z pliku parametry levelu
    nazwa = "level" + str(start_level) + ".txt"
    tilemap.init_from_file(nazwa)  #stworz tablice i okno (szerokosc, dlugosc)

    tilemap_objects.init() #stworzyc obiekty na mapie

