# notifications/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .api.viewsets import NotificationViewSet, NotificationMarkReadView

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = router.urls + [
    path("notifications/mark-read/", NotificationMarkReadView.as_view(), name="notifications-mark-read"),
]