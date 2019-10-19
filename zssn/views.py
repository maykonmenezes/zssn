from zssn.models import Survivor, Inventory, Location, Flag
from zssn.serializers import SurvivorSerializer, InventorySerializer, LastLocationSerializer, FlagSerializer, TradeSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from zssn.permissions import SurvivorReadOnly
from rest_framework.decorators import api_view
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from zssn.reports import Report
from django.shortcuts import get_object_or_404

class SurvivorViewSet(viewsets.ModelViewSet):
    
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    
    def update(self, request):
    	return Response({'status':'Survivor changes not allowed!'}, 
    		status=status.HTTP_405_METHOD_NOT_ALLOWED)

class LastLocationViewSet(viewsets.ModelViewSet):
    
    serializer_class = LastLocationSerializer

    def create(self, request):
    	ls = LastLocationSerializer(data=request.data)
    	survivor = get_object_or_404(Survivor, id=ls.initial_data['survivor_id'])
    	if ls.is_valid():
    		survivor.location.latitude = ls.data['latitude']
    		survivor.location.longitude = ls.data['longitude']
    		survivor.save()
    		return Response({'status':'Survivor last location updated successfully'}, 
    			status=status.HTTP_200_OK)
    	else:
    		return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return None

    def list(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
  

class InventoryViewSet(viewsets.ModelViewSet):
   
   queryset = Inventory.objects.all()
   serializer_class = InventorySerializer
   permission_classes = [SurvivorReadOnly]


class FlagViewSet(viewsets.ModelViewSet):
    
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer

    def create(self, request):
    	fs = FlagSerializer(data=request.data)
    	flagged = get_object_or_404(Survivor, id=fs.initial_data['flagged_id'])
    	flagging = get_object_or_404(Survivor, id=fs.initial_data['flagging_id'])
    	if fs.is_valid():
    		if not flagged == flagging:
	    		flag = Flag()
	    		flag.flagged = flagged
	    		flag.flagging = flagging
	    		flag.save()
	    		return Response({'status':'Survivor flagged as infected successfully!'}, 
	    			status=status.HTTP_200_OK)
	    	else:
	    		return Response({'status':'Survivors cannot flag themselves as infected'}, 
	    			status=status.HTTP_400_BAD_REQUEST)
    	else:
    		return Response(status=status.HTTP_400_BAD_REQUEST)

class ReportViewSet(viewsets.ViewSet):
	
	def list(self, request):
		reports = []
		reports.append(Report.infected())
		reports.append(Report.non_infected())
		reports.append(Report.resource())
		reports.append(Report.lost_points())

		return Response(reports)

class TradeViewSet(viewsets.ModelViewSet):

	serializer_class = TradeSerializer

	def create(self, request):
		ts = TradeSerializer(data=request.data)
		sender = get_object_or_404(Survivor,id=ts.initial_data['sender_id'])
		recipient = get_object_or_404(Survivor,id=ts.initial_data['recipient_id'])
		if ts.is_valid():
			if not sender.infected or not recipient.infected:
				points_sender = (int(ts.data['sender_water']) * 4 + int(ts.data['sender_food']) * 3 +
							 	 int(ts.data['sender_med']) * 2 + int(ts.data['sender_ammo']) * 1)
				points_recipient = (int(ts.data['recipient_water']) * 4 + int(ts.data['recipient_food']) * 3 +
							 		int(ts.data['recipient_med']) * 2 + int(ts.data['recipient_ammo']) * 1)		
				if not sender.inventory.get_points() >= points_sender and not recipient.inventory.get_points() >= points_recipient:
					if points_sender == points_recipient:
						sender.inventory.water -= ts.data['sender_water']
						sender.inventory.food -= ts.data['sender_food']
						sender.inventory.med -= ts.data['sender_med']
						sender.inventory.ammo -= ts.data['sender_ammo']

						recipient.inventory.water -= ts.data['recipient_water']
						recipient.inventory.food -= ts.data['recipient_food']
						recipient.inventory.med -= ts.data['recipient_med']
						recipient.inventory.ammo -= ts.data['recipient_ammo']

						recipient.inventory.water += ts.data['sender_water']
						recipient.inventory.food += ts.data['sender_food']
						recipient.inventory.med += ts.data['sender_med']
						recipient.inventory.ammo += ts.data['sender_ammo']

						sender.inventory.water += ts.data['recipient_water']
						sender.inventory.food += ts.data['recipient_food']
						sender.inventory.med += ts.data['recipient_med']
						sender.inventory.ammo += ts.data['recipient_ammo']

						sender.inventory.save()
						recipient.inventory.save()
						return Response({'status':'Itens traded successfully!'}, 
							status=status.HTTP_200_OK)
					else:
						return Response({'status':'Sorry couldnt make it, one of the traders doesnt have enough points to trade!'}, 
							status=status.HTTP_406_NOT_ACCEPTABLE)
				else:
					return Response({'status':'One of the traders doesnt have enough points to trade!'}, 
						status=status.HTTP_406_NOT_ACCEPTABLE)
			else:
				return Response({'status':'Trade failed due to one of the traders is infected!'}, 
					status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)


	def get_queryset(self):
		return None
       		
					