from library import *
from harvest import *

N = 16
N_MAZE = 1
#N = get_world_size()

substance = N * 2**(num_unlocked(Unlocks.Mazes) - 1)

def make_maze(x, y):
	go_to(x, y)
	plant(Entities.Bush)
	substance = N * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	return measure()

def hug_left():
	pass

def path_find(tx, ty, h=True):
	dir = West
	while get_entity_type() != Entities.Treasure:
		while not can_move(dir):
			dir = turn_right(dir)
		move(dir)
		dir = turn_left(dir)
	if h:
		harvest()
	else:
		use_item(Items.Weird_Substance, substance)

clear()

while True:
	make_maze(0, 0)
		
	for n in range(N_MAZE):
		path_find(0, 0, (n == N_MAZE - 1))

