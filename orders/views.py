# from django.shortcuts import render
from .models import Order, Product, Inventory
from .serializers import OrderSerializer, ProductSerializer, InventorySerializer, OrderStatusSerializer
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAdmin, IsStaff
from django.db.models import Sum


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsStaff]

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [IsStaff]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdmin]

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsStaff]

class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [IsStaff]

class ReportView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, *args, **kwargs):
        total_orders = Order.objects.count()
        total_revenue = (
            Order.objects.aggregate(Sum("total_amount"))["total_amount_sum"] or 0
        )
        low_stock = Inventory.objects.filter(quantity__lt=10).count()
        return Response({
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "low_stock_items": low_stock
        })