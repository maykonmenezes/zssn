from rest_framework import serializers
from zssn.models import Survivor, Inventory, Location, Flag

class InventorySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Inventory
        fields = ['url', 'id', 'survivor', 'water',
                  'food', 'med', 'ammo', 'get_points']
        extra_kwargs = {
            'get_points': {'read_only' : True}, 
            'survivor': {'read_only' : True}
        }

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Location
        fields = ['url', 'id','survivor', 'latitude', 'longitude']
        extra_kwargs = {'survivor': {'read_only' : True}}

class LastLocationSerializer(serializers.Serializer):
    survivor_id = serializers.IntegerField()
    latitude = serializers.DecimalField(decimal_places=6, max_digits=30)
    longitude = serializers.DecimalField(decimal_places=6, max_digits=30)


class FlagSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Flag
        fields = ['url', 'id', 'flagged', 'flagging']

class TradeSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField()
    recipient_id = serializers.IntegerField()
    sender_water = serializers.IntegerField()
    sender_food = serializers.IntegerField()
    sender_medication = serializers.IntegerField()
    sender_ammunition = serializers.IntegerField()
    recipient_water = serializers.IntegerField()
    recipient_food = serializers.IntegerField()
    recipient_medication = serializers.IntegerField()
    recipient_ammunition = serializers.IntegerField()


class SurvivorSerializer(serializers.HyperlinkedModelSerializer):
    inventory = InventorySerializer(many=False)
    location = LocationSerializer(many=False)
    class Meta:
        model = Survivor
        fields = ['url', 'id', 'name', 'age','gender',
                  'infected', 'flags', 'location','inventory']
        extra_kwargs = {
                'flags':{'read_only' : True}, 
                'infected': {'read_only' : True} }


    def create(self, validated_data):
        survivor = Survivor()
        survivor.name = validated_data["name"]
        survivor.age = validated_data["age"]
        survivor.gender = validated_data["gender"]
        survivor.save()
        location = Location()
        location.survivor = survivor
        location.latitude = validated_data["location"]["latitude"] 
        location.longitude = validated_data["location"]["longitude"]
        location.save()
        
        inventory = Inventory()
        inventory.water = validated_data["inventory"]["water"]
        inventory.food = validated_data["inventory"]["food"]
        inventory.med = validated_data["inventory"]["med"]
        inventory.ammo = validated_data["inventory"]["ammo"]
        inventory.survivor = survivor
        inventory.save()
 
        return survivor
