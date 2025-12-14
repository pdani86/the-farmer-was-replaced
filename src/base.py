from common import *

map_size=get_world_size()
w=map_size
h=map_size

pump_size=6
diag_line=13

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


def init_pump():
    till_rect(Grounds.Soil, pump_x, pump_y, pump_size, pump_size)
    
def init_cacti():
    till_rect(Grounds.Soil, cact_x, cact_y, cact_w, cact_h)
    
def init_carrot_tree(enable_trees):
    if enable_trees:
        till_rect_diag(Grounds.Soil, carrot_tree_x, carrot_tree_y, carrot_tree_w,
        carrot_tree_h)
    else:
        till_rect(Grounds.Soil, carrot_tree_x, carrot_tree_y, carrot_tree_w,
        carrot_tree_h)

def plant_pumpkins(xx,yy,size):
    move_to(xx,yy)
    plant_2d(Entities.Pumpkin, size, size, True)


def handle_if_dead_pumpkin():
	e = get_entity_type()
	if e == Entities.Dead_Pumpkin:
		plant(Entities.Pumpkin)
		use_item(Items.Water)
		return False
	return can_harvest()

def harvest_pumpkins(pump_size):
	has_not_ready = True
	row_ok = []
	for i in range(pump_size):
		row_ok.append(False)
	while has_not_ready:
		has_not_ready = False
		for i in range(pump_size):
			if row_ok[i]:
				move(North)
				continue
			this_row_ok = True
			for j in range(pump_size):
				harvestable = handle_if_dead_pumpkin()
				has_not_ready = has_not_ready or not harvestable
				if not harvestable:
					this_row_ok = False
				move(East)
			move_n(West, pump_size)
			row_ok[i] = this_row_ok
			move(North)
		move_n(South, pump_size)
	while not can_harvest():
		do_a_flip()
	harvest()

def do_pumpkins():
    plant_pumpkins(pump_x, pump_y, pump_size)
    move_to(pump_x, pump_y)
    harvest_pumpkins(pump_size)
	
def plant_cacti(x,y,w,h):
    move_to(x, y)
    plant_2d(Entities.Cactus, w, h, True)
	
def do_grass():
    move_to(0, grass_row)
    for i in range(n_grass_pass):
        harv_n(East, w, False)
	
def plant_sun():
    move_to(0, sun_row)
    plant_n(Entities.SunFlower, East, w)
	
def harvest_sun():
    move_to(0, sun_row)
    harv_plant_2d(Entities.SunFlower, East, North, w, n_sun_row, True)
    
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

def init_sun():
    move_to(0, sun_row)
    till_rect(Grounds.Soil, 0, sun_row, w, n_sun_row, True)

def init_fields(enable_trees = True):
	clear()
    init_pump()
    init_cacti()
    init_sun()
    init_carrot_tree(enable_trees)

def init_petals():
    petals = []
    for y in range(h):
        petals.append([])
        row = petals[y]
        for x in range(w):
            row.append(0)
    return petals
    
sun_petals = init_petals()

def plant_sun():
    global sun_petals
    x=get_pos_x()
    y=get_pos_y()
    if plant(Entities.SunFlower):
        sun_petals[y][x] = measure()

def harv_sun():
    global sun_petals
    x=get_pos_x()
    y=get_pos_y()
    if harvest():
        sun_petals[y][x] = 0

def has_row_sun_with_pet_cnt(x0, y, n, cnt):
    global sun_petals
    for i in range(n):
        if sun_petals[y][x0+i]==cnt:
            return True
    return False


def harv_sun_row(x0, y0, n, petal_cnt, dir):
    global sun_petals
    move_to(x0, y0)
    if not has_row_sun_with_pet_cnt(x0, y0, n, petal_cnt):
        return
    for i in range(n):
        if sun_petals[get_pos_y()][get_pos_x()] == petal_cnt:
            harv_sun()
        move(dir)

def plant_sun_rect(x0, y0, ww, hh):
    move_to(x0, y0)
    do_n_2d(East, North, ww, hh, plant_sun)
    
def harv_sun_all_with_cnt(cnt):
    move_to(0, 0)
    for y in range(h):
        harv_sun_row(0, y, w, cnt, East)
    
def harv_sun_all():
    move_to(0, 0)
    for p in range(15, 6, -1):
        harv_sun_all_with_cnt(p)
    
    
def do_sun(x0, y0, ww, hh, n=1):
    for i in range(n):
        plant_sun_rect(x0, y0, ww, hh)
        harv_sun_all()

def do_whole_sun(n=1):
    def f():
        plant(Entities.SunFlower)
        petals[get_pos_y()][get_pos_x()] = measure()
    for i in range(n):
        moveTo(0,0)
        do_n_2d(East, North, w, h, f)


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
