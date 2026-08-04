# notifications/viewsets.py
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Notification
from ..serializers import NotificationSerializer, NotificationMarkReadSerializer


class NotificationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """List-only — notifications aren't created or deleted through this API."""
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationMarkReadView(APIView):
    """POST /api/v1/notifications/mark-read/"""

    def post(self, request):
        serializer = NotificationMarkReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data['ids']

        updated = Notification.objects.filter(id__in=ids, user=request.user).update(is_read=True)

        return Response({'marked_read': updated})