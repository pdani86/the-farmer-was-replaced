from common import *
import base_00
import dyno_00
import maze_00

map_size=get_world_size()
w=map_size
h=map_size


if False:
	n_pump = 1
	n_grass = 1
	enable_trees = False
	base_00.init(n_pump, n_grass, enable_trees)
	#base_00.cycle(1)
	base_00.loop()

if False:
	dyno_00.init()
	dyno_00.loop()

if False:
	clear()
	till_whole(Grounds.Soil)
	while True:
		#do_whole_cacti()
		do_whole_cacti_parallel()

if False:
	maze_00.init()
	maze_00.loop()

if True:
	clear()
	#till_whole(Grounds.Soil)
#	do_till_parallel()
	#do_parallel_simple_harv_plant(Entities.Carrot)
#	g, x0, y0, ww, hh
	till_rect(Grounds.Soil, 0, 0, 32, 4)
	do_parallel_simple_harv_plant(Entities.Carrot, Entities.Grass)
