from common import *

pump_size=6

pump_x=0
pump_y=0

def init_pump():
	move_to(pump_x,pump_y)
	till_rect(Grounds.Soil, pump_x, pump_y, pump_size, pump_size)

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

def do_pumpkins(x, y):
	plant_pumpkins(x, y, pump_size)
	move_to(x, y)
	harvest_pumpkins(pump_size)

def do_pumpkins_parallel(n_w = 2, n_h = 2, block_size = 6):
    drones = []
    def create_f(xx, yy):
        def f():
            plant_pumpkins(xx*(block_size+1), yy*(block_size+1), block_size)
            move_to(xx * (block_size+1), yy * (block_size+1))
            harvest_pumpkins(block_size)
        return f
        
    for yy in range(n_h):
        for xx in range(n_w):
            if xx == 0 and yy == 0:
                continue
            drones.append(spawn_drone(create_f(xx,yy)))
    create_f(0,0)()
    for d in drones:
        wait_for(d)
