def get_harvest_item(e):
	if e == Entities.Grass:
		return Items.Hay
	elif e == Entities.Bush or e == Entities.Tree:
		return Items.Wood
	elif e == Entities.Carrot:
		return Items.Carrot
	elif e == Entities.Pumpkin:
		return Items.Pumpkin
	elif e == Entities.Sunflower:
		return Items.Power
	elif e == Entities.Cactus:
		return Items.Cactus
		
def freeze_inv():
	inv = {}
	for i in Items:
		inv[i] = num_items(i)
	return inv