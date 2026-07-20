from django.urls import path,include

urlpatterns = [
    path("",include("user.urls")),
    path("",include("restaurant.urls")),
    path("",include("menu.urls")),
    path("",include("cart.urls")),
    path("",include("order.urls")),
    path("",include("promotion.urls")),
    path("",include("review.urls")),
    path("",include("favorite.urls")),
    path("",include("notification.urls")),
    path("",include("wallet.urls")),
]