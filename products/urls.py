from django.urls import path
from rest_framework.routers import DefaultRouter
from products.views import InventoryViewSet, ProductViewSet


router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"inventory", InventoryViewSet)

urlpatterns = []

urlpatterns += router.urls

