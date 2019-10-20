from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from zssn.models import Survivor, Inventory, Location, Flag
from django.shortcuts import get_object_or_404

'''
Test cases for the ZSSN API
'''

class SurvivorTests(APITestCase):

    def setUp(self):
        survivor_1 = Survivor(name="Suv 1", age=23, gender="M")
        inv = Inventory(water=4, food=4, med=4, ammo=4) 
        loc = Location(latitude=234235.234,longitude=325235.234)
        survivor_1.inventory = inv
        survivor_1.location = loc
        survivor_1.save()

        survivor_2 = Survivor(name="Suv 2", age=45, gender="F")
        inv = Inventory(water=4, food=4, med=4, ammo=4) 
        loc = Location(latitude=234235.234,longitude=325235.234)
        survivor_2.inventory = inv
        survivor_2.location = loc
        survivor_2.save()

        survivor_3 = Survivor(name="Suv 3", age=23, gender="M")
        inv = Inventory(water=4, food=4, med=4, ammo=4) 
        loc = Location(latitude=234235.234,longitude=325235.234)
        survivor_3.inventory = inv
        survivor_3.location = loc
        survivor_3.save()

        survivor_4 = Survivor(name="Suv 4", age=23, gender="M")
        inv = Inventory(water=4, food=4, med=4, ammo=4) 
        loc = Location(latitude=234235.234,longitude=325235.234)
        survivor_4.inventory = inv
        survivor_4.location = loc
        survivor_4.save()

        survivor_5 = Survivor(name="Suv 5", age=23, gender="M")
        inv = Inventory(water=4, food=4, med=4, ammo=4) 
        loc = Location(latitude=234235.234,longitude=325235.234)
        survivor_5.inventory = inv
        survivor_5.location = loc
        survivor_5.save()


    def test_create_survivor(self):
        data = {
                "name": "Suv 6",
                "age": 26,
                "gender": "M",
                "location": {
                    "latitude": 546546,
                    "longitude": 65465
                },
                "inventory": {
                    "water": 2,
                    "food": 2,
                    "med": 2,
                    "ammo": 2
                }
            }
        response = self.client.post('/survivors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survivor.objects.get(id=1).name, 'Suv 1')
        self.assertEqual(Survivor.objects.get(id=5).gender, 'M')
        self.assertEqual(Survivor.objects.count(), 6)
        self.assertEqual(get_object_or_404(Survivor, id=5).name, 'Suv 5')

    def test_create_survivor_without_location(self):
        data = {"name": "Suv 6",
                "age": 18,
                "gender": "F",
                "inventory": {
                    "water": 4,
                    "food": 4,
                    "med": 4,
                    "ammo": 4
                }
                }
        response = self.client.post('/survivors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Survivor.objects.count(), 5)

    def test_create_survivor_without_inventory(self):
        data = {"name": "Suv 6",
                "age": 18,
                "gender": "F",
                "location": {
                    "latitude": -9879.456456,
                    "longitude": 567567.654654
                }
                }
        response = self.client.post('/survivors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Survivor.objects.count(), 5)

    def test_update_survivor(self):
        data = {
                "name": "Suv 6",
                "age": 16,
                "gender": "F",
                "inventory": {
                    "water": 43,
                    "food": 5,
                    "med": 4,
                    "ammo": 3
                },
                 "location": {
                    "latitude": -9879.456456,
                    "longitude": 567567.654654
                }
                } 
        response = self.client.post('/survivors/5/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Survivor.objects.count(), 5)

    
    def test_update_survivor_location(self):
        data = {
                "latitude": 123,
                "longitude": 123
                }
        response = self.client.post('/survivors/4/last_location/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Survivor.objects.get(id=4).location.longitude,123)

    def test_update_survivor_inventory(self):
        data = {
            'inventory':{
                "water": 43,
                "food": 5,
                "med": 4,
                "ammo": 3
            }     
        } 
        response = self.client.post('/survivors/4/inventory/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_flag_survivor(self):
        data = {
                "flagged_id": 3
                } 
        response = self.client.post('/survivors/1/flag/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Survivor.objects.get(id=3).flags(), 1)

    def test_survivor_flagged_three_times(self):
        data = {
                "flagged_id": 4
                } 
        response = self.client.post('/survivors/1/flag/', data, format='json')
        data = {
                "flagged_id": 4
                } 
        response = self.client.post('/survivors/2/flag/', data, format='json')
        self.assertEqual(Survivor.objects.get(id=4).infected, False)
        data = {
                "flagged_id": 4
                } 
        response = self.client.post('/survivors/3/flag/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Survivor.objects.get(id=4).infected, True)



class TradeTests(APITestCase):

    def setUp(self):
        survivor = Survivor()
        data = {
                "name": "One",
                "age": 23,
                "gender": "M",
                "location": {
                    "latitude": 123,
                    "longitude": 123
                },
                "inventory": {
                    "water": 4,
                    "food": 4,
                    "med": 4,
                    "ammo": 4
                }
            }
        response = self.client.post('/survivors/', data, format='json')

        data = {
                "name": "Two",
                "age": 23,
                "gender": "M",
                "location": {
                    "latitude": 123,
                    "longitude": 123
                },
                "inventory": {
                    "water": 4,
                    "food": 4,
                    "med": 4,
                    "ammo": 4
                }
            }
        response = self.client.post('/survivors/', data, format='json')

        data = {
                "name": "Three",
                "age": 23,
                "gender": "M",
                "location": {
                    "latitude": 123,
                    "longitude": 123
                },
                "inventory": {
                    "water": 4,
                    "food": 4,
                    "med": 4,
                    "ammo": 4
                }
            }
        response = self.client.post('/survivors/', data, format='json')

        data = {
                "name": "Four",
                "age": 23,
                "gender": "M",
                "location": {
                    "latitude": 123,
                    "longitude": 123
                },
                "inventory": {
                    "water": 4,
                    "food": 4,
                    "med": 4,
                    "ammo": 4
                }
            }
        response = self.client.post('/survivors/', data, format='json')
        


    def test_trade_success(self):
        data = {
                "name": "Maykon",
                "age": 23,
                "gender": "M",
                "location": {
                    "latitude": 123,
                    "longitude": 123
                },
                "inventory": {
                    "water": 4,
                    "food": 4,
                    "med": 4,
                    "ammo": 4
                }
            }
        response = self.client.post('/survivors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
                "name": "Larissa",
                "age": 23,
                "gender": "M",
                "location": {
                    "latitude": 123,
                    "longitude": 123
                },
                "inventory": {
                    "water": 4,
                    "food": 4,
                    "med": 4,
                    "ammo": 4
                }
            }
        response = self.client.post('/survivors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
                "buyer_id": 2,
                "pick_water": 3,
                "pick_food": 4,
                "pick_med": 5,
                "pick_ammo": 6,
                "offer_water": 5,
                "offer_food": 4,
                "offer_med": 3,
                "offer_ammo": 2
            }
        response = self.client.post('/survivors/1/trade/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        


    def test_trade_fail(self):
        data = {
            "buyer_id": 2,
            "pick_water": 34,
            "pick_food": 4,
            "pick_med": 5,
            "pick_ammo": 6,
            "offer_water": 5,
            "offer_food": 4,
            "offer_med": 3,
            "offer_ammo": 2
        }
        response = self.client.post('/survivors/1/trade/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_trade_survivor_infected(self):

        data = {
                "flagged_id": 4
                } 
        response = self.client.post('/survivors/1/flag/', data, format='json')
        data = {
                "flagged_id": 4
                } 
        response = self.client.post('/survivors/2/flag/', data, format='json')
        self.assertEqual(Survivor.objects.get(id=4).infected, False)
        data = {
                "flagged_id": 4
                } 
        response = self.client.post('/survivors/3/flag/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Survivor.objects.get(id=4).infected, True)

        data = {
            "buyer_id": 4,
            "pick_water": 3,
            "pick_food": 4,
            "pick_med": 5,
            "pick_ammo": 6,
            "offer_water": 5,
            "offer_food": 4,
            "offer_med": 3,
            "offer_ammo": 2
        }
        response = self.client.post('/survivors/2/trade/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    