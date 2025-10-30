from library import *
from harvest import *

N = get_world_size()

def reset():
	clear()
	go_to(0, 0)
	#plant_chunk(0, 0, N, N, Entities.Grass, True)
	
def main():
	def fer(x, y):
		plant(Entities.Grass)
		use_item(Items.Fertilizer)
		while not can_harvest():
			pass
		harvest()
		
	do_in_chunk(N, N, fer)

while True:
	reset()
	main()