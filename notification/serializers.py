from rest_framework import serializers
from .models import Notification
from user.serializers import UserSerializer


class NotificationReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user','type','title','message','time','action_url','is_read']