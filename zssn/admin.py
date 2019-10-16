from django.contrib import admin
from zssn.models import Survivor, Inventory, LastLocation, Flag
# Register your models here.

admin.site.register(Survivor)
admin.site.register(Inventory)
admin.site.register(LastLocation)
admin.site.register(Flag)