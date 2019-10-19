from zssn.models import Survivor, Inventory, Location, Flag

class Report():

	def infected():
		survivors = Survivor.objects.all()
		infected_survivors = Survivor.objects.filter(infected=True)
		result = {
					"title":"Percentage of Survivors Infected",
					"result": (100.0 /float(len(survivors))) * float(len(infected_survivors))
				  }

		return result


	def non_infected():
		survivors = Survivor.objects.all()
		non_infected_survivors = Survivor.objects.filter(infected = False)
		result = {
					"title":"Percentage of Survivors Non Infected",
					"result": (100.0 /float(len(survivors))) * float(len(non_infected_survivors))
				  }

		return result


	def resource():
		inventories = Inventory.objects.all()
		non_infected_survivors = Survivor.objects.filter(infected = False)
		water = 0
		food = 0
		med = 0
		ammo = 0

		for i in inventories:
			water += i.water
			food += i.food
			med += i.med
			ammo += i.ammo

		result = {
					"title":"Average Amount of Resources by Survivors",
					"result": {
						"water": float(water)/float(len(non_infected_survivors)),
						"food": float(food)/float(len(non_infected_survivors)),
						"med": float(med)/float(len(non_infected_survivors)),
						"ammo": float(ammo)/float(len(non_infected_survivors)),
					}

				  }

		return result


	def lost_points():
		infected_survivors = Survivor.objects.filter(infected=True)
		counter = 0

		for survivor in infected_survivors:
			counter += survivor.inventory.get_points()

		result = {
					"title":"Points Lost Because of Infected Survivors",
					"result": counter
				  }

		return result

		
