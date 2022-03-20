from rest_framework import generics, authentication, permissions
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


class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the authenticated user """
    serializer_class = UserSerializer
    # Gets the authenticated user
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # When the get_object is called the request will have the user attached
    #  to it because of the the authentication classes
    def get_object(self):
        """ Retrieve and return authentication user """
        return self.request.user
