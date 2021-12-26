import pygame
import tilemap
from abc import ABC, abstractmethod


# abstract class
class MovingObject(ABC):
    def __init__(self, img):
        self.x = 0 * tilemap.TILE_SIZE  #x startowy
        self.y = 2 * tilemap.TILE_SIZE  #y startowy
        self.x_vec = 0
        self.y_vec = 0
        self.speed = 0  #predkosc postaci
        self.img = pygame.image.load(img)   #obrazek postaci
        self.img_width, self.img_height = self.img.get_rect().size #rozmiary obrazka postaci

    def draw(self):
        img_x = self.x + (tilemap.TILE_SIZE - self.img_width) / 2 # x postaci
        img_y = self.y + (tilemap.TILE_SIZE - self.img_height) / 2  #y postaci
        tilemap.screen.blit(self.img, (img_x, img_y))   #dodanie postaci do ekranu

    def move(self):
        # check_move() jest uzyta tylko wtedy gdy postac jest dokladnie w kratce
        if self.x % tilemap.TILE_SIZE == 0 and self.y % tilemap.TILE_SIZE == 0:
            self.check_move()
        self.x += self.speed * self.x_vec #przemieszczenie sie postaci w pionie
        self.y += self.speed * self.y_vec   #przemieszczenie sie postaci w poziomie

    def set_speed(self, speed):
        self.speed = speed

    @abstractmethod
    def check_move(self):
        pass

    def action(self):
        self.move()
        self.draw()
