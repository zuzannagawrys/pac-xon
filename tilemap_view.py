import pygame
import tilemap
import stats
import time


textures = {
    14: pygame.image.load('images/apple.png'),      # apple fruit
    13: pygame.image.load('images/sherry.png'),     # sherry fruit
    12: pygame.image.load('images/green.png'),      # green fruit
    11: pygame.image.load('images/lemon.png'),      # lemon fruit
    5: pygame.image.load('images/upper_bar.png'),   # statistics
    4: pygame.image.load('images/occ.png'),         # orange ghost
    3: pygame.image.load('images/marked.png'),      # pacman trace
    2: pygame.image.load('images/occ.png'),         # frame of a map
    1: pygame.image.load('images/occ.png'),         # occupied field
    0: pygame.image.load('images/free.png'),        # free field
    -1: pygame.image.load('images/free.png')        # blue / red / green ghost
}


def draw(): #
    draw_map()
    draw_bar()


def draw_map():
    for row in range(tilemap.HEIGHT):
        for column in range(tilemap.WIDTH):
            tilemap.screen.blit(textures[tilemap.tile_map[row][column]], (column * tilemap.TILE_SIZE, row * tilemap.TILE_SIZE)) #umiesc obrazek na oknie w danych wspolrzednych


heart_red = pygame.image.load('images/heart.png')
heart_blue = pygame.image.load('images/heart_blue.png')
logo = pygame.image.load('images/logo.png')


def draw_bar():
    lives = stats.player_lives #poczatkowe 5 zyc
    max_lives = stats.lives #maksymalne 5 zyc
    for l in range(0, lives):
        tilemap.screen.blit(heart_red, (l * tilemap.TILE_SIZE + 2, tilemap.TILE_SIZE - 2)) #rysowanie czerwonych serduszek na pasku
    for l in range(lives, max_lives):
        tilemap.screen.blit(heart_blue, (l * tilemap.TILE_SIZE + 2, tilemap.TILE_SIZE - 2)) #rysowanie zuzytych serduszek na pasku

    font = pygame.font.SysFont("Ariel", 30)
    text = font.render(str(round(100 * tilemap.marked_fields / tilemap.MAP_FIELDS)) + " %", True, (249, 166, 2)) #procenty postepu
    tilemap.screen.blit(text, ((tilemap.WIDTH - 2) * tilemap.TILE_SIZE + 2, tilemap.TILE_SIZE - 2)) #dodaj procentu postepu do ekranu

    w, h = logo.get_size() #wziecie rozmiaru logo
    tilemap.screen.blit(logo, ((tilemap.WIDTH / 2) * tilemap.TILE_SIZE - w / 2, 0)) #dodanie logo do ekranu



def start_view():
    draw_map() #narysuj mapę z tablicy tilemap

    # ciemniejsze tło
    DARKEN_VAL = 75
    dark = pygame.Surface((tilemap.WIDTH * tilemap.TILE_SIZE, tilemap.HEIGHT * tilemap.TILE_SIZE),
                          flags=pygame.SRCALPHA) #tworzy nowy obraz
    dark.fill((DARKEN_VAL, DARKEN_VAL, DARKEN_VAL)) #wypełnij obraz kolorem
    tilemap.screen.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)  #dodaj obraz ciemnego koloru do ekranu

    #logo
    logo = pygame.image.load('images/logo_huge.png') #stworzenie obrazu loga
    w, h = logo.get_size() #szerokosc i wysokosc loga

    # tekst
    font = pygame.font.SysFont("Ariel", 36)  #ustawienie czcionki
    font.set_bold(True) #pogrubiona czcionka
    text = font.render("CHOOSE LEVEL", True, (249, 166, 2)) #napis kolor
    text_x = tilemap.WIDTH * tilemap.TILE_SIZE / 2 - text.get_rect().width / 2 #wspolrzedna x choose level
    text_y = tilemap.HEIGHT * tilemap.TILE_SIZE * 0.65 #wspolrzedna y choose level
    tilemap.screen.blit(text, (text_x, text_y)) #ustawienie powierzchni tekst na ekranie


    # guziki
    NUM_OF_BUTTONS = 6
    BUTTON_SIZE = 35
    BUTTON_COLOR = (0,0,182)
    BUTTON_SELECTED_COLOR = (124, 221, 255)
    GOLD = (249, 166, 2)
    BUTTON_Y = int(tilemap.HEIGHT * tilemap.TILE_SIZE * 0.85)
    BUTTON_X = int((tilemap.WIDTH * tilemap.TILE_SIZE / 2) - ((NUM_OF_BUTTONS - 1) / 2) * 4 * BUTTON_SIZE)
    button = list()

    for i in range(NUM_OF_BUTTONS):
        x = BUTTON_X + i * 4 * BUTTON_SIZE
        y = BUTTON_Y
        pygame.draw.circle(tilemap.screen, BUTTON_COLOR, (x, y), BUTTON_SIZE) #narysuj guzik
        pygame.draw.circle(tilemap.screen, GOLD, (x, y), BUTTON_SIZE, 5)    #narysuj obwodke wokolo guzika
        number = font.render(str(i + 1), True, GOLD)    #stworz numerek
        number_x = x - number.get_rect().width / 2  #ustaw numerek x
        number_y = y - number.get_rect().height / 2     #ustaw numerek y
        tilemap.screen.blit(number, (number_x, number_y))   #ustaw pozycje numerka na ekranie
        rect = pygame.Rect(x - BUTTON_SIZE,y - BUTTON_SIZE,2 * BUTTON_SIZE,2 * BUTTON_SIZE) #stworzenie prostokątów do klikania
        button.append([rect, BUTTON_COLOR]) #tworzenie listy prostokątów do klikania guzików

    while True:                         #czekamy na klikniecie czegos
        for event in pygame.event.get():    #zostalo klikniete
            if event.type == pygame.QUIT:   #wyjscie
                quit()
            elif event.type == pygame.MOUSEMOTION: #jezeli kursor sie rusza
                for i, b in enumerate(button):
                    if b[0].collidepoint(event.pos): #jezeli kursor myszki jest w prostokacie guzika
                        b[1] = BUTTON_SELECTED_COLOR #zmien kolor guzika na kolor wybrania
                    else:
                        b[1] = BUTTON_COLOR #kolor guzika niezmieniony
            elif event.type == pygame.MOUSEBUTTONUP: #jezeli myszka zostanie kliknieta
                for i, b in enumerate(button): 
                    if b[0].collidepoint(event.pos):  #jezeli guzik zostal klikniety
                        return i + 1    #zwroc numer guzika

        #tworzenie jeszcze raz rzeczy potrzebnych do narysowania ekranu startowego
        draw_map()
        tilemap.screen.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        tilemap.screen.blit(text, (text_x, text_y))
        tilemap.screen.blit(logo, ((tilemap.WIDTH / 2) * tilemap.TILE_SIZE - w / 2, 50))

        for i, b in enumerate(button):
            x, y, s, p = b[0]
            pygame.draw.circle(tilemap.screen, b[1], (x + BUTTON_SIZE, y + BUTTON_SIZE), BUTTON_SIZE)
            pygame.draw.circle(tilemap.screen, GOLD, (x + BUTTON_SIZE, y + BUTTON_SIZE), BUTTON_SIZE, 5)
            number = font.render(str(i + 1), True, GOLD)
            number_x = x + BUTTON_SIZE - number.get_rect().width / 2
            number_y = y + BUTTON_SIZE - number.get_rect().height / 2
            tilemap.screen.blit(number, (number_x, number_y))

        pygame.display.flip() #uaktualnia ekran
        time.sleep(0.1)



DARKEN_VAL = 35
def game_over_view():
    draw_map()
    draw_bar()

    # dim the background
    dark = pygame.Surface((tilemap.WIDTH * tilemap.TILE_SIZE, tilemap.HEIGHT * tilemap.TILE_SIZE),
                          flags=pygame.SRCALPHA)
    dark.fill((DARKEN_VAL, DARKEN_VAL, DARKEN_VAL))
    tilemap.screen.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    # write GAME OVER in the center
    font = pygame.font.SysFont("comicsansms", 72)
    font.set_bold(True)
    text = font.render("GAME OVER", True, (249, 166, 2))
    text_x = tilemap.WIDTH * tilemap.TILE_SIZE / 2 - text.get_rect().width / 2
    text_y = tilemap.HEIGHT * tilemap.TILE_SIZE / 2 - text.get_rect().height / 2
    tilemap.screen.blit(text, (text_x, text_y))

    pygame.display.update()
    pygame.display.flip()

def game_win_view():
    draw_map()
    draw_bar()

    # dim the background
    dark = pygame.Surface((tilemap.WIDTH * tilemap.TILE_SIZE, tilemap.HEIGHT * tilemap.TILE_SIZE),
                          flags=pygame.SRCALPHA)
    dark.fill((DARKEN_VAL, DARKEN_VAL, DARKEN_VAL))
    tilemap.screen.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    # write GAME OVER in the center
    font = pygame.font.SysFont("comicsansms", 72)
    font.set_bold(True)
    text = font.render("LEVEL UP", True, (249, 166, 2))
    text_x = tilemap.WIDTH * tilemap.TILE_SIZE / 2 - text.get_rect().width / 2
    text_y = tilemap.HEIGHT * tilemap.TILE_SIZE / 2 - text.get_rect().height / 2
    tilemap.screen.blit(text, (text_x, text_y))

    pygame.display.update()
    pygame.display.flip()


def clear():
    tilemap.clear()
