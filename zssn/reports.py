from zssn.models import Survivor, Inventory, Location, Flag

class Report():

	infected_survivors = Survivor.object.filter(infected=True)
	survivors = Survivor.object.all()
	inventories = Inventory.object.all()

	def infected():

		result = {
					"title":"Percentage of Survivors Infected",
					"result": (100.0 /float(len(self.survivors))) * float(len(self.survivors_infected))
				  }

		return result


	def non_infected():

		result = {
					"title":"Percentage of Survivors Non Infected",
					"result": (100.0 /float(len(self.survivors_infected))) * float(len(self.survivors))
				  }

		return result


	def resource():

		water = 0
		food = 0
		med = 0
		ammo = 0

		for i in self.inventories:
			water += i.water
			food += i.food
			med += i.med
			ammo += i.ammo

		result = {
					"title":"Average Amount of Resources by Survivors",
					"result": {
						"water": float(water)/float(len(survivors)),
						"food": float(food)/float(len(survivors)),
						"med": float(med)/float(len(survivors)),
						"ammo": float(ammo)/float(len(survivors)),
					}

				  }

		return result


		def lost_points():
			counter = 0
			for survivor in infected_survivors:
				counter += survivor.inventory.get_points()

			result = {
					"title":"Points Lost Because of Infected Survivors",
					"result": counter
				  }

			return result
