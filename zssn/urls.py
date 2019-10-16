from django.urls import path, include
from rest_framework.routers import DefaultRouter
from zssn import views

router = DefaultRouter()
router.register(r'survivors', views.SurvivorViewSet)
router.register(r'inventories', views.InventoryViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'flags', views.FlagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]