from common import *

map_size=get_world_size()
w=map_size
h=map_size

def init():
    clear()
    move_to(0,0)
    pass
    
def cycle():
    pass

def get_no_wrap_dir_from_delta(dx, dy):
    horiz = abs(dx) > abs(dy)
    if horiz:
        if dx < 0:
            return West
        else:
            return East
    else:
        if dy < 0:
            return South
        else:
            return North

def get_no_wrap_dir(x,y):
    dx = x - get_pos_x()
    dy = y - get_pos_y()
    return get_no_wrap_dir_from_delta(dx, dy)

def reset():
    clear()
    move_to(0, 0)
    change_hat(Hats.Straw_Hat)
    change_hat(Hats.Dinosaur_Hat)
    do_a_flip()

def move_towards(x,y):
    dir = get_no_wrap_dir(x, y)
    ok = False
    for i in range(3):
        ok = move(dir)
        if ok:
            break
        dir = dir_to_cw(dir)
    if not ok:
        reset()
        return True
    return (x == get_pos_x()) and (y == get_pos_y())

def move_towards_2(x,y):
# TODO: constant path for long snakes
    def dir_from_pos(xx,yy):
        is_even_row = 0 == yy % 2
        not_edge = x > 0 and y > 0 and x < w-1 and y < h-1
        if not_edge and is_even_row:
            return 
        pass
    move(dir_from_pos(get_pos_x(), get_pos_y()))
    return (x == get_pos_x()) and (y == get_pos_y())

def loop():
    change_hat(Hats.Dinosaur_Hat)
    do_a_flip()
    while True:
        next_x, next_y = measure()
        while not move_towards(next_x, next_y):
            pass
