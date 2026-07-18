from config.viewsets import StandardViewset
from favorite.models import Favorite
from favorite.serializers import FavoriteReadSerializer,FavoriteWriteSerializer

class FavoriteViewset(StandardViewset):
    queryset = Favorite.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create','update']:
            return FavoriteWriteSerializer
        return FavoriteReadSerializer