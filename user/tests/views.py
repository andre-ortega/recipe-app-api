from rest_framework import generics

from user.serializers import UserSerializer

# Using a premade view (createAPI) allowing us to easily make and API that 
#  creates an object in the database using the serializer that we provide

class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    # Easily create
    serializer_class = UserSerializer
