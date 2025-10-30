set_world_size(8)
clear()

a = 0
while True:
	for i in range(8):
		if get_ground_type() == Grounds.Grassland:
			till()

		plant(Entities.Pumpkin)
		if get_entity_type() == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)
			
		if get_entity_type() == Entities.Pumpkin and can_harvest():
			a += 1
		else:
			a = 0
			
		move(North)
	move(East)
	
	if a >= 64:
		harvest()
		a = 0
