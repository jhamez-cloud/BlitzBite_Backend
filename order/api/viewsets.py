from config.viewsets import StandardViewset
from order.models import Order
from order.serializers import OrderReadSerializer,OrderWriteSerializer

class OrderViewset(StandardViewset):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return OrderReadSerializer
        return OrderWriteSerializer