from config.viewsets import StandardViewset
from menu.models import MenuItem
from menu.serializers import MenuItemReadSerializer,MenuItemWriteSerializer

class MenuItemViewset(StandardViewset):
    queryset = MenuItem.objects.all()

    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return MenuItemReadSerializer
        return MenuItemWriteSerializer