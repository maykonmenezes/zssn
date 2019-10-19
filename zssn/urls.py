from django.urls import path, include
from rest_framework.routers import DefaultRouter
from zssn import views

router = DefaultRouter()
router.register(r'survivors', views.SurvivorViewSet)
router.register(r'inventories', views.InventoryViewSet, base_name = 'inventory')
router.register(r'reports',views.ReportViewSet, base_name = 'report')

urlpatterns = [
    path('', include(router.urls)),
]