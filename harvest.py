from library import *

DEFAULT_WATER_LEVEL = 0.5

def plant_chunk(x, y, w, h, e, fer=False, p=False):
	go_to(x, y)
	
	def f(_, _):
		if get_ground_type() != Grounds.Soil:
			till()
		while get_water() < DEFAULT_WATER_LEVEL and num_items(Items.Water) > 0:
			use_item(Items.Water)
		plant(e)
		if fer:
			use_item(Items.Fertilizer)
		
	if p:
		do_in_chunk_p(w, h, f)
	else:
		do_in_chunk(w, h, f)
	

def plant_wood(x, y, w, h, _, _, _):
	def f(x, y):
		while get_water() < DEFAULT_WATER_LEVEL and num_items(Items.Water) > 0:
			use_item(Items.Water)
		if (x+y) % 2 == 0:
			plant(Entities.Tree)
		else:
			plant(Entities.Bush)
			
	do_in_chunk(w, h, f)
	

def plant_maze(x, y, w, h, _, _, _):
	go_to(x, y)
	plant(Entities.Bush)
	substance = w * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)


def harvest_maze(_, _, w, _, h=True, p=False):
	dir = West
	while get_entity_type() != Entities.Treasure:
		while not can_move(dir):
			dir = turn_right(dir)
		move(dir)
		dir = turn_left(dir)
	harvest()
	#substance = w * 2**(num_unlocked(Unlocks.Mazes) - 1)
	#use_item(Items.Weird_Substance, substance)


def harvest_basic(x, y, w, h, fer=False, p=False):
	last_crop_type = None
	
	def f(x, y):
		last_crop_type = None
		ground_type = get_ground_type()
		crop_type = get_entity_type()
		while crop_type and not can_harvest():
			continue
		harvest()
		if crop_type == None:
			if last_crop_type != None:
				crop_type = last_crop_type
			else:
				if coin_flip():
					crop_type = Entities.Grass
				else:
					crop_type = Entities.Bush
		if not can_plant(crop_type, 1):
			if coin_flip():
				crop_type = Entities.Grass
			else:
				crop_type = Entities.Bush
		if crop_type != Entities.Grass and ground_type != Grounds.Soil:
			till()
		while get_water() < DEFAULT_WATER_LEVEL and num_items(Items.Water) > 0:
			use_item(Items.Water)
			
		plant(crop_type)
		if fer:
			use_item(Items.Fertilizer)
		last_crop_type = crop_type
	
	if p:
		do_in_chunk_p(w, h, f)
	else:
		do_in_chunk(w, h, f)


def harvest_pumpkin_patch(x, y, w, h, _, _):
	dead = []
	
	go_to(x, y)
		
	for i in range(w):
		for j in range(h):
			while not can_harvest() and get_entity_type() != Entities.Dead_Pumpkin:
				pass
			if get_entity_type() == Entities.Dead_Pumpkin:
				dead.append((x+i, y+j))
				plant(Entities.Pumpkin)
			if j < h-1:
				move(North)
		move_n_dir(h-1, South)
		if i < w-1:
			move(East)
	move_n_dir(w-1, West)
	
	while len(dead) > 0:
		dest_idx = nearest_point_idx((get_pos_x(), get_pos_y()), dead, 1)
		go_to(dead[dest_idx][0], dead[dest_idx][1])
		
		if get_entity_type() == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)
			
		elif can_harvest():
			dead.pop(dest_idx)
	
	harvest()


def harvest_sunflowers(x, y, w, h, _, _):
	levels = []
	
	def f(x, y):
		while not can_harvest():
			pass
		value = measure()
		inserted = False
		if len(levels) == 0:
			levels.append((x, y, value))
			return
		for i in range(len(levels)):
			if value > levels[i][2]:
				levels.insert(i, (x, y, value))
				inserted = True
				break
		if not inserted:
			levels.append((x, y, value))
	
	do_in_chunk(w, h, f)
	
	for target in levels:
		go_to(x+target[0], y+target[1])
		harvest()
		#plant(Entities.Sunflower)
		

def harvest_cactus(_, _, w, h, _, _):
	values = []
	
	for i in range(w):
		values.append([])
		for j in range(h):
			values[i].append([])
			while not can_harvest():
				pass
			values[i][j] = measure()
			if j < h-1:
				move(North)
		move_n_dir(h-1, South)
		if i < w-1:
			move(East)
	move_n_dir(w-1, West)

	changes = 1
	while changes > 0:
		changes = 0
		for x in range(w):
			for y in range(h):
				swaps = 0
				while y < (len(values[0]) - 1) and values[x][y] > values[x][y+1]:
					swaps += 1
					swap(North)
					move(North)
					temp = values[x][y]
					values[x][y] = values[x][y+1]
					values[x][y+1] = temp
				move_n_dir(swaps, South)
				changes += swaps
					
				if y < h-1:
					move(North)
			move_n_dir(h-1, South)
			if x < w-1:
				move(East)
		move_n_dir(w-1, West)
		
		for y in range(h):
			for x in range(w):
				swaps = 0
				while x < (len(values) - 1) and values[x][y] > values[x+1][y]:
					swaps += 1
					swap(East)
					move(East)
					temp = values[x][y]
					values[x][y] = values[x+1][y]
					values[x+1][y] = temp
				move_n_dir(swaps, West)
				changes += swaps
					
				if x < w-1:
					move(East)
			move_n_dir(w-1, West)
			if y < h-1:
				move(North)
		move_n_dir(h-1, South)

	harvest()