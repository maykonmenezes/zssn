from django.urls import path, include
from rest_framework.routers import DefaultRouter
from zssn import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'survivors', views.SurvivorViewSet)
router.register(r'inventories', views.InventoryViewSet)
router.register(r'last-locations', views.LastLocationViewSet)
router.register(r'flags', views.FlagViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]