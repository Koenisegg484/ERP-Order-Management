from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

class BootstrapUserView(APIView):
    """
    TEMPORARY endpoint – remove after initial setup
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        secret = request.headers.get("X-BOOTSTRAP-KEY")

        if secret != settings.BOOTSTRAP_SECRET:
            return Response({"detail": "Unauthorized"}, status=401)

        user = User.objects.create_superuser(
            username=request.data["username"],
            email=request.data.get("email", ""),
            password=request.data["password"]
        )

        return Response({"id": user.id, "username": user.username})
