import ghost
import random
import pygame
import numpy
from scipy.ndimage import label
import control
import tilemap_objects

TILE_SIZE = 24
tile_map = []
WIDTH = 0
HEIGHT = 0
screen = None

MAP_FIELDS = 0
marked_fields = 0


def init_from_file(file):
    global tile_map, WIDTH, HEIGHT, screen, MAP_FIELDS, marked_fields
    tile_map = numpy.array([[int(n) for n in line.split()] for line in open(file, "r")])
    WIDTH = len(tile_map[0])
    HEIGHT = len(tile_map)
    MAP_FIELDS = WIDTH * HEIGHT - 2 * (WIDTH + HEIGHT) - WIDTH + 4
    marked_fields = 0
    screen = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE))


def init(width, height):
    global tile_map, WIDTH, HEIGHT, screen, MAP_FIELDS, marked_fields 
    #     tablica pol, szer, dl,    okno,   ?????,      ?????
    WIDTH = width
    HEIGHT = height
    MAP_FIELDS = WIDTH * HEIGHT - 2 * (WIDTH + HEIGHT) - WIDTH + 4
    marked_fields = 0
    menu_bar = [[5] * WIDTH]
    interior = [[2] + [0] * (WIDTH - 2) + [2]]
    margin = [[2] * WIDTH]
    tile_map = numpy.array(2 * menu_bar + margin + (HEIGHT - 4) * interior + margin) #tablica pol
    screen = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE)) #tworzy okno do grania w danych rozmiarach


def row_num(x):
    return int(x / TILE_SIZE)


def col_num(y):
    return int(y / TILE_SIZE)


def mark_path(path): #dodaje pola oznaczone przez pacmana do bezpiecznych pol
    global marked_fields, MAP_FIELDS
    marked_fields += len(path)
    while path:
        (x, y) = path.pop()
        tile_map[y][x] = 1
    if round(100 * marked_fields / MAP_FIELDS) > 80:
        control.win()

@tilemap_objects.check_win_decorator
def mark_area():
    global marked_fields
    s = [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]]


    a = numpy.array(tile_map) #bierze tablice pol
    labeled_array, num_features = label(a <= 0, structure=s) #zwraca tablicę z zaznaczonymi obszarami wolnych miejsc kazdy oznaczonymi innymi numerami, bezpieczne pola oznaczone 0

    # jeżeli mamy wiecej niz jeden zamkniety obszar
    if num_features > 1:
        # dla kazdego obszaru
        for i in range(1, num_features + 1):
            labeled_list = list(zip(*numpy.where(labeled_array == i))) #tworzymy liste pol ktore zawiera

            # sprawdzamy czy mamy przeszkode w tym obszarze
            is_obstacle = [True for (x, y) in labeled_list if tile_map[x][y] == -1]

            #jezeli nie ma przeszkody
            if not is_obstacle:
                marked_fields += len(labeled_list) #dodajemy ilosc  pol w obszarze do ilosci zaznaczonych pol

                for (x, y) in labeled_list: #oznaczamy na mapie obszar jako bezpieczny
                    tile_map[x][y] = 1
                tilemap_objects.add_orange_ghost(random.sample(labeled_list, 1)) #dodaje pomaranczowego duszka jezeli ma byc dodany


def clear():
    global tile_map
    tile_map = None
    init(WIDTH, HEIGHT)
    tilemap_objects.clear()
    tilemap_objects.init()