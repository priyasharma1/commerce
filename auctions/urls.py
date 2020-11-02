from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all", views.all_listings, name="all"),
    path("category/<str:category>", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new"),
    path("edit/<str:id>", views.edit_listing, name="edit"),
    path("delete/<str:id>", views.delete, name="delete"),
    path("create", views.create_listing, name="create"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("watch/<str:id>", views.watch, name="watch"),
    path("watchlist", views.watch_list, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("comment/<str:id>", views.delete_comment, name="comment"),
    path("delete/bid/<str:id>", views.delete_bid, name="delete_bid")
]
