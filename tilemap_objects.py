import tilemap
import ghost
import pacman
import stats
import control
import not_moving_objects


player = None
objects = list()

orange_ghosts_num = 0


def init():
    global orange_ghosts_num, player

    player = pacman.Pacman() #stworzenie pacmana gracza

    for i in range(stats.blue_ghosts_num): #stworzenie niebieskich duszkow (podstawowe)
        objects.append(ghost.BlueGhost())   #dodanie duszka do listy obiektow

    for i in range(stats.red_ghosts_num):   #stworzenie czerwonych duszkow (jedzące pola gracza)
        objects.append(ghost.RedGhost())    #dodanie duszka do listy obiektow

    for i in range(stats.green_ghosts_num): #stworzenie zielonych duszkow (poruszajace sie wzdluż krawedzi)
        objects.append(ghost.GreenGhost())  #dodanie duszka do listy obiektow

    orange_ghosts_num = stats.orange_ghosts_num #ustawienie globalnie liczby pomaranczowych duchow

    not_moving_objects.start_fruit_thread() #zaczac watek tworzenia owockow


def action():
    player.action() #metoda wywolywana z moving_objects

    for o in objects:
        o.action() #metoda wywolywana z moving_objects


def add_orange_ghost(pos): #dodaje pomaranczowego duszka jezeli ma byc dodany
    global orange_ghosts_num

    if orange_ghosts_num > 0:
        y_ind, x_ind = pos[0]
        if tilemap.tile_map[y_ind][x_ind] != 1:
            return
        objects.append(ghost.OrangeGhost(x_ind, y_ind))
        orange_ghosts_num -= 1


def check_win_decorator(function):
    def wrapper():
        func = function()

        if round(100 * tilemap.marked_fields / tilemap.MAP_FIELDS) > 80:
            player.reset_position()
            control.win()
        else:
            return func
    return wrapper


def check_loss_decorator(function):
    def wrapper():
        func = function()

        if stats.player_lives == 0:
            control.game_over()
            stats.player_lives = stats.lives
            player.reset_position()
        else:
            return func
    return wrapper


@check_loss_decorator
def kill_player(): #
    player.reset_position()
    stats.player_lives -= 1 

def clear():
    global player, objects, orange_ghosts_num
    player = None
    del objects[:]


def set_pacman_speed(speed):
    while True:
        if player.x % tilemap.TILE_SIZE == 0 and player.y % tilemap.TILE_SIZE == 0:
            player.set_speed(speed)
            return

def set_ghost_speed(speed):
    for o in objects:
            while True:
                if o.x % tilemap.TILE_SIZE == 0 and o.y % tilemap.TILE_SIZE == 0:
                    o.set_speed(speed)
                    break
