from config.viewsets import StandardViewset
from notification.models import Notification
from notification.serializers import NotificationReadSerializer,NotificationWriteSerializer

class NotificationViewset(StandardViewset):
    queryset = Notification.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return NotificationReadSerializer
        return NotificationWriteSerializer