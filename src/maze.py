from common import *

map_size=get_world_size()
w=map_size
h=map_size

maze_x=15
maze_y=15
maze_size=20

def init():
    pass

def cycle(n):
    pass
    
def create_maze():
    move_to(maze_x, maze_y)
    plant(Entities.Bush)
    substance = maze_size * 2**(num_unlocked(Unlocks.Mazes) - 1)
    use_item(Items.Weird_Substance, substance)

def solve_maze():
    last_dir = North
    while get_entity_type() != Entities.Treasure:
        dir = dir_to_cw(last_dir)
        ok = move(dir)
        if not ok:
            dir=last_dir
            ok = move(dir)
        if not ok:
            dir=dir_to_ccw(last_dir)
            ok = move(dir)
        if not ok:
            dir = opp_dir(last_dir)
            ok = move(dir)
        if ok:
            last_dir = dir
    harvest()

def loop():
    while True:
        clear()
        create_maze()
        solve_maze()


