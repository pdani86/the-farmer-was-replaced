dir_order_cw = [North,East,South,West]

map_size=get_world_size()
w=map_size
h=map_size

def find_ix(list, val):
	for i in range(len(list)):
		if list[i] == val:
			return i
	return None

def get_dir_ix(dir):
	return find_ix(dir_order_cw, dir)

def opp_dir(dir):
	return dir_order_cw[(get_dir_ix(dir)+2)%4]

def dir_to_cw(dir):
	return dir_order_cw[(get_dir_ix(dir)+1)%4]
	
def dir_to_ccw(dir):
	return dir_order_cw[(get_dir_ix(dir)+3)%4]

def is_horiz(dir):
	if dir==East or dir==West:
		return True
	return False


def do_work_parallel(func_factory, max_drones, n_task):
	task_ix = 0
	while task_ix < n_task:
		drones = []
		n_task_in_cycle = min(n_task - task_ix, max_drones)
		for i in range(n_task_in_cycle-1):
			drones.append(spawn_drone(func_factory(task_ix+i+1)))
		func_factory(task_ix)()
		for d in drones:
			wait_for(d)
		task_ix += n_task_in_cycle


def move_n(dir, n):
	if n>map_size/2:
		dir = opp_dir(dir)
		n = map_size - n
	for i in range(n):
		move(dir)

def move_to(xx, yy):
	allow_wrap = True
	x_dir = East
	y_dir = North
	dx = xx-get_pos_x()
	dy = yy-get_pos_y()
	if (dx > w/2) or ((dx < 0) and (dx > -1*w/2)):
		x_dir = West
	if (dy > h/2) or ((dy < 0) and (dy > -1*h/2)):
		y_dir = South
		
	while get_pos_x()!=xx:
		move(x_dir)
	while get_pos_y()!=yy:
		move(y_dir)

def get_diag_type(x, y):
	return (x+y)%2

def do_n(dir, n, func, ret = True):
	for i in range(n):
		func()
		move(dir)
	if ret:
		move_n(opp_dir(dir), n)
		
def do_n_2d(dir_1, dir_2, n, m, func, ret = True):
	for i in range(m):
		do_n(dir_1, n, func)
		move(dir_2)
	if ret:
		move_n(opp_dir(dir_2), m)

def till_to(g):
	if get_ground_type() == g:
		return
	till()

def till_rect(g, x0, y0, ww, hh, ret=True):
	def t():
		till_to(g)
	move_to(x0,y0)
	for i in range(hh):
		do_n(East, ww, t)
		move(North)
	if ret:
		move_n(South, hh)

def till_rect_diag(g, x0, y0, ww, hh):
	def tt():
		till_to(g)
	move_to(x0,y0)
	for i in range(hh):
		for j in range(ww):
			t = get_diag_type(x0+j,y0+i)
			if t == 0:
				tt()
			move(East)
		move(North)

def harv_n(dir, n, ret = True):
	do_n(dir, n, harvest, ret)

def harv_plant(item, dir, n, ret = True):
	def h_p():
		harvest()
		plant(item)
	do_n(dir, n, h_p, ret)

def harv_plant_2d(item, dir_1, dir_2, n, m, ret = True):
	for i in range(m):
		harv_plant(item, dir_1, n)
		move(dir_2)
	if ret:
		move_n(opp_dir(dir_2), m)
	
def plant_n(item, dir, n, ret = True):
	def p():
		plant(item)
	do_n(dir, n, p, ret)

def plant_2d(item, ww, hh, ret = False):
	for i in range(hh):
		plant_n(item, East, ww)
		move(North)
	if ret:
		move_n(South, hh)

def bubble_step(dir, n, ord = True):
	is_sorted = True
	for i in range(n):
		here = measure()
		next = measure(dir)
		if (next!=here) and ((next<here) == ord):
			swap(dir)
			is_sorted = False
		move(dir)
	return is_sorted

def sort(dir, n):
	o_dir = opp_dir(dir)
	for k in range(n-1):
		is_sorted = True
		kk = n-k-1
		is_sorted = bubble_step(dir, kk, True)
		#is_sorted = bubble_step(o_dir, kk, False)
		move_n(o_dir, kk)
		if is_sorted:
			return

def sort_2d(dir_1, dir_2, n, m):
	sort(dir_1, n)
	sort(dir_2, m)

def sort_cacti(x0, y0, ww, hh):
	move_to(x0, y0)
	for i in range(ww):
		sort(North, hh)
		move(East)
	move_to(x0, y0)
	for i in range(hh):
		sort(East, ww)
		move(North)
		
def sort_cacti_h_v(x0, y0, n, horiz):
	move_to(x0, y0)
	if horiz:
		sort(East, n)
	else:
		sort(North, n)

def sort_parellel_func(x,y,size,i, horiz):
	if not horiz:
		sort_cacti_h_v(x+i, y, size, horiz)
	else:
		sort_cacti_h_v(x, y+i, size, horiz)

def sort_cacti_parallel_square_(x, y, size, horiz, max_drones):
	def work_factory(ix):
		def f():
			move_to(x,y+ix)
			sort_parellel_func(x, y, size, ix, horiz)
		return f
	do_work_parallel(work_factory, max_drones, size)
	

def sort_cacti_parallel_square(x, y, size, max_drones):
	sort_cacti_parallel_square_(x, y, size, False, max_drones)
	sort_cacti_parallel_square_(x, y, size, True, max_drones)
		
def harvest_cacti(x,y,w,h):
	sort_cacti(x, y, w, h)
	move_to(x, y)
	harvest()
	
def harvest_cacti_parallel(x, y, size, max_drones):
	sort_cacti_parallel_square(x, y, size, max_drones)
	harvest()

def till_whole(g):
	till_rect(g, 0, 0, w, h)

def do_whole_cacti():
	move_to(0,0)
	plant_2d(Entities.Cactus, w, h)
	harvest_cacti(0, 0, w, h)
		
def plant_parallel(x,y,rows,cols, item = Entities.Cactus, max_drones = 32):
	def work_factory(ix):
		def f():
			move_to(x,y+ix)
			plant_n(item, East, cols, False)
		return f
	do_work_parallel(work_factory, max_drones, rows)
	
def harvest_parallel(x,y,rows,cols, item = Entities.Cactus, max_drones = 32):
	def work_factory(ix):
		def f():
			move_to(x,y+ix)
			harv_n(East, cols, False)
		return f
	do_work_parallel(work_factory, max_drones, rows)

def do_whole_cacti_parallel(max_drones = 32):
	move_to(0,0)
	plant_parallel(0, 0, w, h, Entities.Cactus, max_drones)
	harvest_cacti_parallel(0, 0, w, max_drones)
	
def do_square_cacti_parallel(s, max_drones = 32):
	move_to(0,0)
	plant_parallel(0, 0, s, s, Entities.Cactus, max_drones)
	harvest_cacti_parallel(0, 0, s, max_drones)

def repeat_row_plant(y, size, soil_item, grass_item):
	move_to(0, y)
	while(True):
		for i in range(size):
			if can_harvest():
				harvest()
			else:
				do_a_flip()
				harvest()
			item = grass_item
			if get_ground_type() == Grounds.Soil:
				item = soil_item
			if item != Entities.Grass:
				plant(item)
			move(East)

def do_till_parallel(max_drones = 1, bottom_row = 0, width = get_world_size(), height = get_world_size()):
	clear()
	
	row = bottom_row
	remaining_rows = height
	
	def work_factory(ix):
		def f():
			till_rect(Grounds.Soil, 0, bottom_row+ix, width, 1)
		return f
	
	do_work_parallel(work_factory, max_drones, height)


def do_parallel_simple_harv_plant(soil_item = Entities.Carrot, grass_item = Entities.Tree, size = get_world_size()):
	#do_till_parallel()
	drones = []
	def soil_item_from_row_ix(ix):
		return soil_item
		
	def grass_item_from_row_ix(ix):    
		return grass_item
		
	for i in range(size-1):
		def f():
			repeat_row_plant(i, size, soil_item_from_row_ix(i), grass_item_from_row_ix(i))
		drones.append(spawn_drone(f))
	repeat_row_plant(size-1, size, soil_item_from_row_ix(size-1), grass_item_from_row_ix(size-1))