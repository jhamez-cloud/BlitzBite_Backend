# favorites/viewsets.py
from django.db.migrations import serializer
from httpx import request
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from ..models import Favorite
from ..serializers import FavoriteSerializer


class FavoriteViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('restaurant')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        restaurant_id = kwargs.get('pk')
        deleted, _ = Favorite.objects.filter(restaurant_id=restaurant_id, user=request.user).delete()
        
        if not deleted:
            return Response({'detail': 'Favorite not found.'}, status=404)
        return Response(status=204)