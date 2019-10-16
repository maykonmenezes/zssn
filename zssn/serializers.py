from rest_framework import serializers
from zssn.models import Survivor, Inventory, LastLocation, Flag

    #owner = serializers.ReadOnlyField(source='owner.username')
    #highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    #snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

class SurvivorSerializer(serializers.HyperlinkedModelSerializer):
    inventory = serializers.HyperlinkedRelatedField(many=False, view_name='inventory-detail', read_only=True)
    lastlocation = serializers.HyperlinkedRelatedField(many=False, view_name='last-location-detail', read_only=True)
    class Meta:
        model = Survivor
        fields = ['url', 'id', 'name', 'age', 'lastlocation',
                  'gender','infected', 'flags', 'inventory']


class InventorySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Inventory
        fields = ['url', 'id', 'survivor', 'water',
                  'food', 'med', 'ammo']

class LastLocationSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = LastLocation
        fields = ['url', 'id','survivor', 'latitude', 'longitude']

class FlagSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Flag
        fields = ['url', 'id', 'flagged', 'flagging']