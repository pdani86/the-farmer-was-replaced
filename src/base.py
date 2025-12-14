from common import *
import * from sunflower
import * from pumpkins

map_size=get_world_size()
w=map_size
h=map_size

diag_line=13

pump_size=6
pump_x=0
pump_y=0

# all east of pumpkin row
#cact_x=pump_size
#cact_y=0
#cact_w=w-pump_size
#cact_h=pump_size

# less columns
#cact_y=0
#cact_w=3
#cact_x=w-cact_w
#cact_h=pump_size

# all in pumpkin row
cact_x=0
cact_y=0
cact_w=w
cact_h=pump_size

sun_row=pump_size
n_sun_row=3
grass_row=sun_row+n_sun_row
n_grass_pass=20

carrot_tree_x=0
carrot_tree_y=10
carrot_tree_w=w
carrot_tree_h=h-carrot_tree_y

    
def init_cacti():
    till_rect(Grounds.Soil, cact_x, cact_y, cact_w, cact_h)
    
def init_carrot_tree(enable_trees):
    if enable_trees:
        till_rect_diag(Grounds.Soil, carrot_tree_x, carrot_tree_y, carrot_tree_w,
        carrot_tree_h)
    else:
        till_rect(Grounds.Soil, carrot_tree_x, carrot_tree_y, carrot_tree_w,
        carrot_tree_h)

def plant_cacti(x,y,w,h):
    move_to(x, y)
    plant_2d(Entities.Cactus, w, h, True)
	
def do_grass():
    move_to(0, grass_row)
    for i in range(n_grass_pass):
        harv_n(East, w, False)

    
def harv_carrot_tree():
    def f():
        harvest()
        g = get_ground_type()
        if g == Grounds.Soil:
            item = Entities.Carrot
        else:
            item = Entities.Tree
        plant(item)
    move_to(carrot_tree_x, carrot_tree_y)
    do_n_2d(East, North, carrot_tree_w, carrot_tree_h, f)

def init_fields(enable_trees = True):
	clear()
    init_pump()
    init_cacti()
    init_sun()
    init_carrot_tree(enable_trees)

n_pumpkin_cycle = 1

def init(n_pump = 1, n_grass = 1, enable_trees = True):
    global n_grass_pass
    global n_pumpkin_cycle
    n_grass_pass = n_grass
    n_pumpkin_cycle = n_pump
    clear()
    #till_whole(Grounds.Soil)
    #do_sun(0,0, w, h, 100)
    #do_whole_cacti()
    init_fields(enable_trees) # False: no trees
    move_to(0, 0)

def cycle(n):
    for i in range(n):
        for j in range(n_pumpkin_cycle):
            do_pumpkins()
        #plant_cacti(cact_x, cact_y, cact_w, cact_h)
        plant_sun_rect(0, sun_row, w, n_sun_row)
        do_grass()
        harv_sun_all()
        #harvest_cacti(cact_x, cact_y, cact_w, cact_h)
        harv_carrot_tree()
        move_to(0, 0)
    

def loop():
    while True:
        cycle(1)
