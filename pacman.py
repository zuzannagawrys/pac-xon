import pygame
import tilemap
import control
import tilemap_objects
from moving_objects import MovingObject
import not_moving_objects


class Pacman(MovingObject):
    def __init__(self):
        super().__init__('images/pacman_prawo.png')
        self.speed = 6 #ustawienie predkosci
        self.marked_tiles = []  #dodanie wlasnosci zaznaczonych plytek

    def check_move(self):
        x_ind = tilemap.row_num(self.x + self.img_width / 2) #kolumna kratki w ktorej jest pacman
        y_ind = tilemap.col_num(self.y + self.img_height / 2) #rzad kratki w ktorej jest pacman
        self.update_position(x_ind, y_ind) #uaktualnia kratke w ktorej jest pacman i go zabija jesli trzeba

        key = pygame.key.get_pressed()

        # pacman moze sie zatrzymac dopiero jezeli jest na swoim polu
        if tilemap.tile_map[y_ind][x_ind] not in [0, 11, 12, 13, 14]: #jezeli pacman jest na swoim polu
            direction = (0, 0) #zatrzymuje sie
        else: 
            direction = (self.x_vec, self.y_vec) #w innym przypadku musi kontunuowac ruch

        if key[pygame.K_RIGHT]:
            direction = (1, 0) #zmiana kierunku w prawo
            self.img = pygame.image.load('images/pacman_prawo.png') #zmiana zwrotu postaci
        elif key[pygame.K_LEFT]:
            direction = (-1, 0) #zmiana kierunku w lewo
            self.img = pygame.image.load('images/pacman_lewo.png')
        elif key[pygame.K_DOWN]:
            direction = (0, 1) #zmiana kierunku w dol
            self.img = pygame.image.load('images/pacman_dol.png')
        elif key[pygame.K_UP]:
            direction = (0, -1) #zmiana kierunku w gore
            self.img = pygame.image.load('images/pacman_gora.png')

        (self.x_vec, self.y_vec) = direction #przypisanie kierunku do atrybutow

        # zabezpiecza przed wyjsciem poza plansze
        if tilemap.tile_map[self.y_ind][self.x_ind] == 2:
            if y_ind == 2:
                self.y_vec = max(0, self.y_vec)
            elif y_ind == tilemap.HEIGHT - 1:
                self.y_vec = min(0, self.y_vec)
            if x_ind == 0:
                self.x_vec = max(0, self.x_vec)
            elif x_ind == tilemap.WIDTH - 1:
                self.x_vec = min(0, self.x_vec)

        if tilemap.tile_map[self.y_ind+self.y_vec][self.x_ind+self.x_vec] == -2:
            if self.y_vec < 0:
                self.y_vec = max(0, self.y_vec)
            else:
                self.y_vec = min(0, self.y_vec)
            if self.x_vec <0:
                self.x_vec = max(0, self.x_vec)
            else:
                self.x_vec = min(0, self.x_vec)


        # jezeli pacman zjadl owoc
        if tilemap.tile_map[self.y_ind][self.x_ind] in [11, 12, 13, 14]:
            not_moving_objects.fruit_action(tilemap.tile_map[self.y_ind][self.x_ind])

        # zaznacza sciezke pacmana
        self.mark_tile(x_ind, y_ind)

    def mark_tile(self, x_ind, y_ind):
        if tilemap.tile_map[y_ind][x_ind] in [0, 11, 12, 13, 14]: #jezeli pole jest puste lub ma owoc
            tilemap.tile_map[y_ind][x_ind] = 3 #oznacz pole jako zaznaczone przez pacmana
            self.marked_tiles.append((x_ind, y_ind)) #dodaj pole do zaznaczonych pol pacmana
        elif self.marked_tiles: #jezeli mamy zaznaczone pola a znajdujemy sie na polu bezpiecznym
            tilemap.mark_area() #zaznacza pola bezpieczne i dodaje pomaranczowe duszki jezeli jest potrzeba
            tilemap.mark_path(self.marked_tiles.copy()) #dodaje pola oznaczone przez pacmana do bezpiecznych pol
            del self.marked_tiles[:] #usuniecie zaznaczonych pol

    def update_position(self, new_x, new_y):
        if tilemap.tile_map[new_y][new_x] in [-1, 3, 4]: #jezeli pacman natrafi na duszka albo swoj slad
            tilemap_objects.kill_player() 
        else:
            self.x_ind, self.y_ind = new_x, new_y #uaktualnia kratke w ktorej jest pacman

    def reset_position(self):
        self.x = 0 * tilemap.TILE_SIZE
        self.y = 2 * tilemap.TILE_SIZE

        self.x_vec = 0
        self.y_vec = 0

        path = self.marked_tiles.copy() #kopiuje wczesniej zaznaczone pola
        del self.marked_tiles[:] #usuwa liste zaznaczonych pol pacmana
        while path:
            (x, y) = path.pop()
            tilemap.tile_map[y][x] = 0 #usuwa pola zaznaczone przez pacmana na ekranie
