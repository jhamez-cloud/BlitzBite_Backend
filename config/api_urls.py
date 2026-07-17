from django.urls import path,include

urlpatterns = [
    path("", include("user.urls")),
    path("", include("restaurant.urls")),
    path("",include("menu.urls")),
    path("",include("cart.urls")),
]