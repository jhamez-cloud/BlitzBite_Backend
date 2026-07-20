# users/views.py
from config.viewsets import StandardViewset
from user.models import User, Address, PaymentMethod
from user.serializers import UserSerializer, AddressSerializer, PaymentMethodSerializer


class UserViewSet(StandardViewset):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddressViewSet(StandardViewset):
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user_id=self.kwargs['user_pk'])

    def perform_create(self, serializer):
        serializer.save(user_id=self.kwargs['user_pk'])


class PaymentMethodViewSet(StandardViewset):
    serializer_class = PaymentMethodSerializer

    def get_queryset(self):
        return PaymentMethod.objects.filter(user_id=self.kwargs['user_pk'])

    def perform_create(self, serializer):
        serializer.save(user_id=self.kwargs['user_pk'])