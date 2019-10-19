from django.urls import path, include
from rest_framework.routers import DefaultRouter
from zssn import views

router = DefaultRouter()
router.register(r'survivors', views.SurvivorViewSet)
router.register(r'inventories', views.InventoryViewSet, base_name = 'inventory')
router.register(r'location', views.LastLocationViewSet, base_name = 'location')
router.register(r'flag-infected', views.FlagViewSet, base_name = 'flag')
router.register(r'reports',views.ReportViewSet, base_name = 'report')
router.register(r'trades',views.TradeViewSet, base_name = 'trade')

urlpatterns = [
    path('', include(router.urls)),
]