from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("createlisting/", views.create_listing, name="createlisting"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("closelisting/<int:id>", views.close_listing, name="closelisting"),
    path("categories/", views.categories, name="categories"),
    path("category/<int:name>", views.category, name="category"),
    path("listing/<int:list_id>/comment/", views.comment, name="comment"),
    path("listing/<int:list_id>/bid/", views.bid, name="bid"),
    path("watchlists/listing/", views.watchlists, name="watchlists"),
    path("addwatchlist/listing/<int:id>/", views.addWatchlist, name="addWatchlist"),
    path("removewatchlist/listing/<int:id>/", views.removeWatchlist, name="removeWatchlist"),
]
