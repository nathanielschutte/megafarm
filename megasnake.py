from library import *
from harvest import *

def reset():
	clear()
	change_hat(Hats.Wizard_Hat)

def main():
	go_to(0, 0)
	change_hat(Hats.Dinosaur_Hat)
	while True:
		move(North)
		for x in range(get_world_size()):
			dir = North
			if x % 2 == 1:
				dir = South
			move_n_dir(get_world_size()-2, dir)
			move(East)
		move(South)
		if not go_to(0, 0):
			change_hat(Hats.Wizard_Hat)
			go_to(0, 0)
			change_hat(Hats.Dinosaur_Hat)
		#x, y = measure()
		#while go_to(x, y):
			#x, y = measure()

reset()
main()	