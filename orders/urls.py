from django.urls import path
from .views import OrderCreateView, OrderListView, ProductViewSet, InventoryViewSet, OrderStatusUpdateView, ReportView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"inventory", InventoryViewSet)

urlpatterns = [
    path("orders/", OrderListView.as_view()),
    path("orders/create/", OrderCreateView.as_view()),
    path("orders/<int:pk>/status/", OrderStatusUpdateView.as_view()),
    path("orders/reports/", ReportView.as_view())
]

urlpatterns += router.urls


# a680c1f720312e388ec5e2b6eb643f55713e1a97 for erp_owner