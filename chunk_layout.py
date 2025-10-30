from library import *
from harvest import *
from metrics import *

METRICS_N = 2

MEGA_SUN = [
	[0, 0, 8, 8, Entities.Sunflower, plant_chunk, harvest_sunflowers, True],
	[8, 8, 8, 8, Entities.Sunflower, plant_chunk, harvest_sunflowers, True],
	[0, 8, 4, 4, Entities.Cactus, plant_chunk, harvest_cactus, True],
]

MAIN = [
	[0, 6, 2, 22, Entities.Bush, plant_wood, harvest_basic, False],
	[2, 6, 3, 16, Entities.Carrot, plant_chunk, harvest_basic, False],
	[6, 0, 16, 6, Entities.Grass, plant_chunk, harvest_basic, False],
	
	# Pumpkin patches
	[0, 0, 6, 6, Entities.Pumpkin, plant_chunk, harvest_pumpkin_patch, True],
	[5, 6, 6, 6, Entities.Pumpkin, plant_chunk, harvest_pumpkin_patch, True],
	[10, 12, 6, 6, Entities.Pumpkin, plant_chunk, harvest_pumpkin_patch, True],
	
	# Sunflowers
	[11, 6, 11, 6, Entities.Sunflower, plant_chunk, harvest_sunflowers, True],
	
	# Cactus
	[5, 12, 6, 6, Entities.Cactus, plant_chunk, harvest_cactus, True],
	
	# Maze
	#[21, 21, 6, 6, Entities.Bush, plant_maze, harvest_maze, True],
]

TEST = [
	[0, 0, 4, 4, Entities.Bush, plant_chunk, harvest_basic, False],
	[0, 4, 4, 4, Entities.Bush, plant_chunk, harvest_basic, False],
]

main_layout = MAIN

def farm(layout):
	clear()
	
	quick_print('')
	quick_print('')
	quick_print('NEW FARM!')

	N = max_drones()
	drones = []
	drone_tasks = []
	
	task_count = len(layout)
	if N > task_count:
		N = task_count
	shard_len = task_count // N
	shard_rem = task_count % N
	shard_count = task_count // shard_len
	
	for i in range(N):
		drone_tasks.append([])
	
	for i in range(task_count):
		task = layout[i]
		bucket = i // shard_len
		drone_tasks[bucket].append(task)
	
	for i in range(task_count):
		task = layout[i]
		if i < len(layout) - shard_rem:
			continue
		drone_tasks[N-1].append(task)
	
	first_plant = True
	while True:
		drones = []
		
		inv = freeze_inv()
	
		for i in range(N):
			def work():
				global first_plant
				#for _ in range(METRICS_N):
				while True:
					for chunk in drone_tasks[i]:
						if first_plant or chunk[7]:
							go_to(chunk[0], chunk[1])
							chunk[5](chunk[0], chunk[1], chunk[2], chunk[3], chunk[4], False, False)
							
						go_to(chunk[0], chunk[1])
						chunk[6](chunk[0], chunk[1], chunk[2], chunk[3], False, False)
					
					first_plant = False

			if i < N - 1:
				drones.append(spawn_drone(work))
			else:
				work()
			
		for drone in drones:
			wait_for(drone)
			
		replant = freeze_inv()
		
		quick_print('HARVESTS SINCE METRICS:', METRICS_N)
		for i in Items:
			diff = replant[i] - inv[i]
			quick_print(i, ':', diff)
		
		quick_print('')
		quick_print('NEXT HARVEST')
			

def farm_sync(layout):
	clear()
	
	quick_print('')
	quick_print('')
	quick_print('NEW FARM!')
	for chunk in layout:
		go_to(chunk[0], chunk[1])
		chunk[5](chunk[0], chunk[1], chunk[2], chunk[3], chunk[4], False, False)

	# harvest + replant
	while True:
		inv = freeze_inv()
		
		for chunk in layout:
			go_to(chunk[0], chunk[1])
			chunk[6](chunk[0], chunk[1], chunk[2], chunk[3])
			
		harvest = freeze_inv()
			
		for chunk in layout:
			# needs a replant
			if chunk[7]:
				go_to(chunk[0], chunk[1])
				chunk[5](chunk[0], chunk[1], chunk[2], chunk[3], chunk[4])
				
		replant = freeze_inv()
				
		for i in Items:
			diff = replant[i] - inv[i]
			quick_print(i, ':', diff)
		
		quick_print('NEXT HARVEST')
		quick_print('')
		

clear()
farm(main_layout)