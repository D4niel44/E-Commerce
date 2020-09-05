from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("login", auth_views.LoginView.as_view()),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/toogle_watchlist",
         views.toogle_watchlist,
         name="toogle_watchlist"),
    path("listing/<int:listing_id>/close",
         views.close_listing,
         name="close_listing"),
    path("listing/<int:listing_id>/post_comment",
         views.post_comment,
         name="post_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
]
