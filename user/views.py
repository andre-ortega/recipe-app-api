from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer

# Using a premade view (createAPI) allowing us to easily make and API that 
#  creates an object in the database using the serializer that we provide

class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    # Easily create
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for user """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
