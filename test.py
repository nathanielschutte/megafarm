from harvest import *
from library import *

N = 16

clear()
plant_chunk(0, 0, N, N, Entities.Bush, True, True)
while True:
	harvest_basic(0, 0, N, N, True, True)