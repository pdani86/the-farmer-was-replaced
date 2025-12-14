from common import *

def init_sun():
	move_to(0, sun_row)
	till_rect(Grounds.Soil, 0, sun_row, w, n_sun_row, True)

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
		plant_sun()
	for i in range(n):
		move_to(0,0)
		do_n_2d(East, North, w, h, f)
	harv_sun_all()

def do_whole_sun_until(n=1000):
	if num_items(Items.Power) >= n:
		return
	till_whole(Grounds.Soil)
	while num_items(Items.Power) < n:
		do_whole_sun()

