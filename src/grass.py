from common import *

def do_parallel_grass_rows(n_drone = 16):
	def repeat_line_harvest():
		while True:
			harvest()
			move(East)
	clear()
	drones = []
	for i in range(n_drone-1):
		def f():
			move_to(0,i+1)
			repeat_line_harvest()
		drones.append(spawn_drone(f))
	move_to(0,0)
	repeat_line_harvest()
    