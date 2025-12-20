from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework import status

User = get_user_model()

class BootstrapUserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    parser_classes = [JSONParser]

    def post(self, request):
        key = request.headers.get("X-BOOTSTRAP-KEY")

        if key != settings.BOOTSTRAP_SECRET:
            return Response({"detail": "Invalid bootstrap key"}, status=403)

        if User.objects.filter(is_superuser=True).exists():
            return Response({"detail": "Admin already exists"}, status=400)

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "Missing credentials"}, status=400)

        User.objects.create_superuser(
            username=username,
            password=password
        )

        return Response({"message": "Admin created"}, status=201)
