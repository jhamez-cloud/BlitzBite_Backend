from config.viewsets import StandardViewset
from cart.models import CartItem
from cart.serializers import CartItemReadSerializer,CartItemWriteSerializer

class CartItemViewset(StandardViewset):
    queryset = CartItem.objects.all()

    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return CartItemReadSerializer
        return CartItemWriteSerializer