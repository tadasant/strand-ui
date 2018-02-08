from rest_framework.authtoken.views import ObtainAuthToken
from app.api.serializers import CustomAuthTokenSerializer


class CustomObtainAuthTokenView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
