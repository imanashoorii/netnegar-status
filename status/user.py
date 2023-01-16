from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import User
from .userSerializer import UserMeSerializer


class UserMe(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserMeSerializer

    def get_object(self):
        return self.request.user
