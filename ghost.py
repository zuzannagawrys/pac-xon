import pygame
import tilemap
import tilemap_objects
from random import choice, randint
from abc import ABC, abstractmethod
from moving_objects import MovingObject


# abstract class
class Ghost(MovingObject, ABC):
    def __init__(self, img):
        super().__init__(img)
        self.id = -1    #nowa wlasciwosc duszka id
        self.speed = 3 #predkosc duszka 3
        self.starting_position()
        self.x_vec = choice([-1, 1])    # strona w ktora sie porusza w poziomie
        self.y_vec = choice([-1, 1])    # strona w ktora sie porusza w pionie
        self.x_ind = tilemap.row_num(self.x)    #pozycja x w kratkach
        self.y_ind = tilemap.col_num(self.y)    #pozycja y w kratkach

    def starting_position(self):
        while(True):
            indx= randint(5,tilemap.WIDTH - 5)
            x=indx* tilemap.TILE_SIZE + 0.5 * tilemap.TILE_SIZE  # ustawienie pozycji duszka na dowolnym miejscu planszy x
            indy=randint(5,tilemap.HEIGHT - 5)
            y = indy * tilemap.TILE_SIZE + 0.5 * tilemap.TILE_SIZE  # ustawienie pozycji duszka na dowolnym miejscu planszy y
            if tilemap.tile_map[indy][indx]==0:
                self.x=x
                self.y=y
                return


    def check_move(self):
        x_ind = tilemap.row_num(self.x + self.img_width / 2) 
        y_ind = tilemap.col_num(self.y + self.img_height / 2)
        self.update_position(x_ind, y_ind)

        collisions = 0
        collides = self.check_collision() #sprawdzamy czy bedzie kolizja
        while collides:
            self.handle_collision(collides) #obsługujemy kolizję
            
            if collisions == 8: # jezeli duszek utknie zamrazamy go
                self.speed = 0
                self.img = pygame.image.load('images/frozen_ghost.png')
                collides = False
            else:
                collisions += 1
                collides = self.check_collision()

    def update_position(self, new_x, new_y):
        old_x, old_y = self.x_ind, self.y_ind
        tilemap.tile_map[old_y][old_x] = 0
        tilemap.tile_map[new_y][new_x] = self.id
        self.x_ind, self.y_ind = new_x, new_y

    @abstractmethod
    def check_collision(self):
        pass

    @abstractmethod
    def handle_collision(self, colliding_vec):
        pass



class PinkGhost(Ghost):
    """Podstawowy duszek"""
    def __init__(self, img='images/pink_ghost.png'):
        super().__init__(img)

    def check_collision(self):
        # natepne pole w poziomie
        if tilemap.tile_map[self.y_ind][self.x_ind + self.x_vec] > 0 or tilemap.tile_map[self.y_ind][self.x_ind + self.x_vec]==-2:
            return self.x_vec, 0
        # nastepne pole w pionie
        elif tilemap.tile_map[self.y_ind + self.y_vec][self.x_ind] > 0 or tilemap.tile_map[self.y_ind + self.y_vec][self.x_ind]==-2:
            return 0, self.y_vec
        # nastepny rog
        elif tilemap.tile_map[self.y_ind + self.y_vec][self.x_ind + self.x_vec] > 0 or tilemap.tile_map[self.y_ind + self.y_vec][self.x_ind + self.x_vec]== -2:
            return self.x_vec, self.y_vec
        else:
            return ()

    def handle_collision(self, colliding_vec):
        x_col, y_col = colliding_vec #wektory ktore koliduja
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] in [1, 2, -2]: #jezeli nastepne pole jest sciana
            # zmien kierunek poruszania sie
            if x_col:
                self.x_vec = -self.x_vec
            if y_col:
                self.y_vec = -self.y_vec
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] == 3: #jezeli anstepne pole jest sciezka pacmana zabij gracza
            tilemap_objects.kill_player()
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] in [11, 12, 13, 14]: #jezeli nastepne pole jest owockiem zniszcz go
            tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] = 0

class RedGhost(PinkGhost):
    """Duszek zjadający bezpieczne pola gracza"""
    def __init__(self):
        super().__init__('images/redd_ghost.png')
        self.speed=2;

    def handle_collision(self, colliding_vec):
        x_col, y_col = colliding_vec
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] == 1: #jezeli zderzasz sie z polami stworzonymi przez gracza
            # zmien kierunek poruszania sie
            if x_col:
                self.x_vec = -self.x_vec
            if y_col:
                self.y_vec = -self.y_vec
            # znisz bezbieczne pola gracza z ktorymi sie zderzasz
            tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] = 0
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] in [2,-2]: #jezeli zderzasz sie z krawedziami mapy
            # zmien kierunek poruszania sie
            if x_col:
                self.x_vec = -self.x_vec
            if y_col:
                self.y_vec = -self.y_vec
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] == 3: #jezeli anstepne pole jest sciezka pacmana zabij gracza
            tilemap_objects.kill_player()
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] in [11, 12, 13, 14]: #jezeli nastepne pole jest owockiem zniszcz go
            tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] = 0


class OrangeGhost(Ghost):
    """Duszek poruszający się wzdłuż pól gracza"""
    def __init__(self):
        super().__init__('images/oorange_ghost.png')
        self.x_ind = tilemap.WIDTH - 2
        self.y_ind = tilemap.HEIGHT - 2
        self.x_vec = choice([-1, 0])
        self.y_vec = 0 if self.x_vec else -1
        self.x = self.x_ind * tilemap.TILE_SIZE + self.x_vec * self.speed
        self.y = self.y_ind * tilemap.TILE_SIZE + self.y_vec * self.speed
        self.changed_dir = 0

    def check_collision(self):
        if tilemap.tile_map[self.y_ind + self.y_vec][self.x_ind + self.x_vec] > 0 or tilemap.tile_map[self.y_ind + self.y_vec][self.x_ind + self.x_vec] ==-2: #jezeli przed duszkiem jest przeszkoda
            return self.x_vec, self.y_vec
        elif not self.changed_dir and tilemap.tile_map[self.y_ind - self.x_vec][self.x_ind + self.y_vec] == 0: #jeżeli pod duszkiem nie ma pol gracza
            return self.y_vec, -self.x_vec
        else:
            self.changed_dir = 0
            return ()

    def handle_collision(self, colliding_vec):
        x_col, y_col = colliding_vec
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] == 0:
            # zmien kierunek poruszania sie
            if y_col:
                self.y_vec = -self.x_vec
                self.x_vec = 0
            if x_col:
                self.x_vec = self.y_vec
                self.y_vec = 0
            self.changed_dir = 1
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] in [1, 2, -2]:
            # zmien kierunek poruszania sie
            if x_col:
                self.y_vec = self.x_vec
                self.x_vec = 0
            if y_col:
                self.x_vec = -self.y_vec
                self.y_vec = 0
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] == 3: #jezeli anstepne pole jest sciezka pacmana zabij gracza
            tilemap_objects.kill_player()
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] in [11, 12, 13, 14]: #jezeli nastepne pole jest owockiem zniszcz go
            tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] = 0



class BlueGhost(Ghost):
    """Duszek poruszający sie w bezpiecznych obszarach gracza"""
    def __init__(self, x_ind, y_ind):
        super().__init__('images/light_blue_ghost.png')
        self.id = 4
        self.x_ind = x_ind
        self.y_ind = y_ind
        self.x = x_ind * tilemap.TILE_SIZE + 0.5 * tilemap.TILE_SIZE
        self.y = y_ind * tilemap.TILE_SIZE + 0.5 * tilemap.TILE_SIZE
    #odbija sie od krawedzi pustych przestrzeni i krawedzi planszy
    def check_collision(self):
        if tilemap.tile_map[self.y_ind][self.x_ind + self.x_vec] in [0, 2, -2]:
            return self.x_vec, 0
        elif tilemap.tile_map[self.y_ind + self.y_vec][self.x_ind] in [0, 2, -2]:
            return 0, self.y_vec
        elif tilemap.tile_map[self.y_ind + self.y_vec][self.x_ind + self.x_vec] in [0, 2, -2]:
            return self.x_vec, self.y_vec
        else:
            return ()

    def handle_collision(self, colliding_vec):
        x_col, y_col = colliding_vec
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] in [0, 2, -2]:
            # zmien kierunek poruszania sie
            if x_col:
                self.x_vec = -self.x_vec
            if y_col:
                self.y_vec = -self.y_vec
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] == 3: #jezeli anstepne pole jest sciezka pacmana zabij gracza
            tilemap_objects.kill_player()
        if tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] in [11, 12, 13, 14]: #jezeli nastepne pole jest owockiem zniszcz go
            tilemap.tile_map[self.y_ind + y_col][self.x_ind + x_col] = 1



    def update_position(self, new_x, new_y):
        old_x, old_y = self.x_ind, self.y_ind
        tilemap.tile_map[old_y][old_x] = 1
        tilemap.tile_map[new_y][new_x] = self.id
        self.x_ind, self.y_ind = new_x, new_y
