def coin_flip():
	return ((random()*2) // 2) == 0

def go_home():	
	for i in range(get_pos_x()):
		move(West)
	for i in range(get_pos_y()):
		move(South)
	
def move_n_dir(n, dir):
	for i in range(n):
		if not move(dir):
			return False
	return True

def reverse_dir_idx(i):
	return [North, South, East, West][i + (1 - 2 * (i % 2))]
	
def turn_right(dir):
	if dir == North:
		return East
	elif dir == East:
		return South
	elif dir == South:
		return West
	elif dir == West:
		return North
		
def turn_left(dir):
	if dir == East:
		return North
	elif dir == North:
		return West
	elif dir == West:
		return South
	elif dir == South:
		return East
	
def go_to(x, y):
	start_x = get_pos_x()
	start_y = get_pos_y()
	if start_x < x:
		if not move_n_dir(x - start_x, East):
			return False
	elif start_x > x:
		if not move_n_dir(start_x - x, West):
			return False
	if start_y < y:
		if not move_n_dir(y - start_y, North):
			return False
	elif start_y > y:
		if not move_n_dir(start_y - y, South):
			return False
	return True

def nearest_point_idx(source, points, radius=0):
	close_idx = -1
	close_dist = -1
	idx = 0
	if len(points) < 1:
		return None
	for point in points:
		xd = (point[0] - source[0])**2
		yd = (point[1] - source[1])**2
		distance = (xd + yd)**(1/2)
		if distance >= radius and (close_dist == -1 or distance < close_dist):
			close_idx = idx
			close_dist = distance
		idx += 1
	return close_idx

def can_plant(en, n):
	cost = get_cost(en)
	for e in cost:
		v = cost[e]
		if num_items(e) < v*n:
			return False
	return True

def do_in_chunk(w, h, f):
	for i in range(w):
		for j in range(h):
			f(i, j)
			if j < h-1:
				move(North)
		move_n_dir(h-1, South)
		if i < w-1:
			move(East)
	move_n_dir(w-1, West)
	

def do_in_chunk_p(w, h, f):
	N = max_drones() - num_drones()
	ox, oy = get_pos_x(), get_pos_y()
	#N = max_drones()
	#N = 8

	if N > w:
		N = w
	
	shard_width = w//N
	shard_count = w//shard_width
	w = shard_width

	drones = []
	
	for c in range(shard_count):
		x = c*shard_width
		y = oy
		
		def work():
			go_to(x, y)
			for i in range(w):
				for j in range(h):
					f(i, j)
					if j < h-1:
						move(North)
				move_n_dir(h-1, South)
				if i < w-1:
					move(East)
			move_n_dir(w-1, West)
		
		if c == (shard_count - 1):
			# syncronous so do last
			work()
		else:
			spawn = spawn_drone(work)
			if spawn == None:
				quick_print('spawn drone error: None')
				return None
			drones.append(spawn)
	
	for d in drones:
		wait_for(d)
	
	go_to(ox, oy)