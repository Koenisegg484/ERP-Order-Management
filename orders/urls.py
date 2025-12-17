from django.urls import path
from .views import OrderCreateView, OrderListView, OrderStatusUpdateView, ReportView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:pk>/status/", OrderStatusUpdateView.as_view(), name="order-status-update"),
    path("orders/reports/", ReportView.as_view(), name="order-reports"),
]

# a680c1f720312e388ec5e2b6eb643f55713e1a97 for erp_owner