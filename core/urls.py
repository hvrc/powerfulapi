from django.urls import path
from . import views

urlpatterns = [
    path("refresh/", views.refreshStaticDatabase, name="refreshStaticDatabase"),
    path("", views.viewStaticDatabase, name="viewStaticDatabase"),
]
