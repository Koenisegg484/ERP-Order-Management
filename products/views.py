from django.shortcuts import render
from rest_framework import viewsets
from config.permissions import IsAdmin, IsStaff
from products.models import Inventory, Product
from products.serializers import InventorySerializer, ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdmin]
    

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsStaff]
