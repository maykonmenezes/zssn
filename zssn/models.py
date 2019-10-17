from django.db import models

GENDER_CHOICES = (('M', 'MALE'), ('F', 'FEMALE'))

class Survivor(models.Model):

    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    infected = models.BooleanField(default=False)

    class Meta:
    	verbose_name = 'Survivor'
    	verbose_name_plural = 'Survivors'

    def __str__(self):
    	return self.name

    def flags(self):
    	return len(self.flagged.all())


class Inventory(models.Model):

	survivor = models.OneToOneField(Survivor, related_name="inventory", on_delete=models.CASCADE)
	water = models.IntegerField(default=0)
	food = models.IntegerField(default=0)
	med = models.IntegerField(default=0)
	ammo = models.IntegerField(default=0)

	class Meta:
		verbose_name = 'Inventory'
		verbose_name_plural = 'Inventories'

	def __str__(self):
		return self.survivor.name + " Inventory"

    def get_points(self):
        return water*4 + food*3 + med*3 + ammo


class Location(models.Model):
	latitude = models.FloatField(default=0)
	longitude = models.FloatField(default=0)
	survivor = models.OneToOneField(Survivor, related_name="location", on_delete=models.CASCADE)
	

class Flag(models.Model):
    flagged = models.ForeignKey(Survivor, related_name="flagged", on_delete=models.CASCADE)
    flagging = models.ForeignKey(Survivor, related_name="flagging", on_delete=models.CASCADE)

    def save(self):
        if(self.flagged != self.flagging):
            flags = Flag.objects.filter(flagging = self.flagging, flagged = self.flagged).all()
            if (len(flags) <= 0):
                super().save()
            if(self.flagged.flags() >= 3):
                self.flagged.infected = True
                self.flagged.save()

