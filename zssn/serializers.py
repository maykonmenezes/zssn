from rest_framework import serializers
from zssn.models import Survivor, Inventory, Location, Flag


class SurvivorSerializer(serializers.HyperlinkedModelSerializer):
    inventory = serializers.HyperlinkedRelatedField(many=False, view_name='inventory-detail', read_only=True)
    location = serializers.HyperlinkedRelatedField(many=False, view_name='location-detail', read_only=True)
    class Meta:
        model = Survivor
        fields = ['url', 'id', 'name', 'age', 'location',
                  'gender','infected', 'flags', 'inventory']


class InventorySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Inventory
        fields = ['url', 'id', 'survivor', 'water',
                  'food', 'med', 'ammo']

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Location
        fields = ['url', 'id','survivor', 'latitude', 'longitude']

class FlagSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Flag
        fields = ['url', 'id', 'flagged', 'flagging']