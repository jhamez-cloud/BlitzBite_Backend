# users/views.py
from config.viewsets import StandardViewset
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User, Address, PaymentMethod
from user.serializers import UserRegistrationSerializer, UserSerializer, AddressSerializer, PaymentMethodSerializer


class UserViewSet(StandardViewset):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterView(APIView):
    def post(self, request):
        user = request.user  # already exists via get_or_create in the auth class
        serializer = UserRegistrationSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(user).data, status=201)


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