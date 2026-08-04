# notifications/serializers.py
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    icon = serializers.ReadOnlyField()

    class Meta:
        model = Notification
        fields = ['id', 'type', 'title', 'message', 'time', 'is_read', 'action_url', 'icon']
        read_only_fields = fields
        # Entirely read-only — notifications are created by backend business
        # logic (order status changes, promo campaigns, etc.), never by a
        # user POSTing one directly.


class NotificationMarkReadSerializer(serializers.Serializer):
    """POST /notifications/mark-read/ — body: { ids: [...] }"""
    ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)