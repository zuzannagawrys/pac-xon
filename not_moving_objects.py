import pygame
import tilemap
from abc import ABC
import random
import threading
import time
import control
import tilemap_objects


ID_LIST = [11, 12, 13, 14]



def get_position():
    x = random.randint(3, tilemap.WIDTH - 3)
    y = random.randint(5, tilemap.HEIGHT - 5)

    while tilemap.tile_map[y][x]:
        x = random.randint(3, tilemap.WIDTH - 3)
        y = random.randint(5, tilemap.HEIGHT - 5)
    return x, y


def draw_on_a_map(x, y):
    id = random.choice(ID_LIST)
    tilemap.tile_map[y][x] = id

def erase_from_a_map(x, y):
    tilemap.tile_map[y][x] = tilemap.tile_map[y][x+1]

def control_fruit():
    while not control.done: #watek spi przez randomowa ilosc czasu
        t = random.randint(2, 10)
        while t:
            time.sleep(1)
            if control.done:
                return
            t -= 1
        x, y = get_position() #wylosowac randomowa pozycje
        draw_on_a_map(x, y) #narysowanie w tej pozycji randomowego owocka
        time.sleep(random.randint(4, 6)) #watek spi przez randomowa ilosc czasu
        erase_from_a_map(x, y)  #owocek sie kasuje


def start_fruit_thread():
    thread_1 = threading.Thread(target=control_fruit, daemon=True)
    thread_1.start()
    thread_2 = threading.Thread(target=control_fruit, daemon=True)
    thread_2.start()
    thread_3 = threading.Thread(target=control_fruit, daemon=True)
    thread_3.start()


def fruit_action(id):
    thread = threading.Thread(target=control_action, args=(id,))
    thread.start()
    thread.join


def control_action(id):
    if id == 11:
        thread_4 = threading.Thread(target=tilemap_objects.set_pacman_speed, args=(3,))
        thread_4.start()
        thread_4.join()
        time.sleep(5)
        thread_4 = threading.Thread(target=tilemap_objects.set_pacman_speed, args=(6,))
        thread_4.start()
        thread_4.join()
    if id == 12:
        thread_5 = threading.Thread(target=tilemap_objects.set_pacman_speed, args=(8,))
        thread_5.start()
        thread_5.join()
        time.sleep(5)
        thread_5 = threading.Thread(target=tilemap_objects.set_pacman_speed, args=(6,))
        thread_5.start()
        thread_5.join()
    if id == 13:
        tilemap_objects.set_ghost_speed_0()
        time.sleep(5)
        tilemap_objects.set_normal_ghost_speed_0()
    if id == 14:
        thread_7 = threading.Thread(target=tilemap_objects.set_ghost_speed,args=(1,))
        thread_7.start()
        thread_7.join()
        time.sleep(5)
        thread_7 = threading.Thread(target=tilemap_objects.set_normal_ghost_speed)
        thread_7.start()
        thread_7.join()
