from library import *
from harvest import *

N = 8
#N = get_world_size()

substance = N * 2**(num_unlocked(Unlocks.Mazes) - 1)

def reset():
	clear()
	go_to(0, 0)
	plant(Entities.Bush)
	substance = N * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	
def path_find(src, tx, ty, n):
	if get_entity_type() == Entities.Treasure:
		if n > 0:
			use_item(Items.Weird_Substance, substance)
			tx, ty = measure()
			n = n - 1
		else:
			harvest()
			return True
	
	x = get_pos_x()
	y = get_pos_y()
	
	options = []
	dirs = [(North, (0, 1)), (South, (0, -1)), (East, (1, 0)), (West, (-1, 0))]
	idx = 0
	for d in dirs:
		if can_move(d[0]):
			dest = (x+d[1][0], y+d[1][1])
			if not (dest[0] == src[0] and dest[1] == src[1]):
				options.append((d[0], d[1]))
		idx += 1
			
	if len(options) == 0:
		return False
		
	sort_options = []
	for o in options:
		s = o[1][0] * (tx - x) + o[1][1] * (ty - y)
		if len(sort_options) == 0:
			sort_options.append((o[0], s))
		else:
			for i in range(len(sort_options)):
				if s >= sort_options[i][1]:
					sort_options.insert(i, (o[0], s))
	
	for o in sort_options:
		go_to(x, y)
		src = (x, y)
		move(o[0])
		if path_find(src, tx, ty, n):
			return True
	
	return False
			
	
while True:
	reset()
	treasure_x, treasure_y = measure()
	path_find((0, 0), treasure_x, treasure_y, 2)
	