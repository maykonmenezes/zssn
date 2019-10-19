from rest_framework import serializers
from zssn.models import Survivor, Inventory, Location, Flag

class InventorySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Inventory
        fields = ['id', 'water',
                  'food', 'med', 'ammo', 'get_points']
        extra_kwargs = {
            'get_points': {'read_only' : True}, 
            'survivor': {'read_only' : True}
        }


class LocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Location
        fields = ['id','latitude', 'longitude']
        extra_kwargs = {'survivor': {'read_only' : True}}

class LastLocationSerializer(serializers.Serializer):

    latitude = serializers.DecimalField(decimal_places=6, max_digits=30)
    longitude = serializers.DecimalField(decimal_places=6, max_digits=30)


class FlagSerializer(serializers.Serializer):

    flagged_id = serializers.IntegerField()

class TradeSerializer(serializers.Serializer):

    buyer_id = serializers.IntegerField()

    pick_water = serializers.IntegerField()
    pick_food = serializers.IntegerField()
    pick_med = serializers.IntegerField()
    pick_ammo = serializers.IntegerField()

    offer_water = serializers.IntegerField()
    offer_food = serializers.IntegerField()
    offer_med = serializers.IntegerField()
    offer_ammo = serializers.IntegerField()


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
