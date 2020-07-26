from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.detail, name="detail"),
    path("edit/<str:entryTitle>", views.edit, name="edit"),
    path("random", views.random_entry, name="random"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search")
]
