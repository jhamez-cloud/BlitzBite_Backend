from user.models import User
from config.viewsets import StandardViewset
from user.serializers import UserReadSerializer, UserWriteSerializer

class UserViewset(StandardViewset):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return UserReadSerializer
        return UserWriteSerializer