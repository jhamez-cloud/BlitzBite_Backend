from config.viewsets import StandardViewset
from restaurant.models import Restaurant
from restaurant.serializers import RestaurantReadSerializer, RestaurantWriteSerializer

class RestaurantViewset(StandardViewset):
    queryset = Restaurant.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RestaurantReadSerializer
        return RestaurantWriteSerializer