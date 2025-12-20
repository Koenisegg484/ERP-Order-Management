from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from config.views import BootstrapUserView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("orders.urls")),
    path('api/', include("products.urls")),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path("bootstrap/create-admin/", BootstrapUserView.as_view()),

]
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]