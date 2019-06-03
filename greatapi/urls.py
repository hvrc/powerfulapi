from django.urls import path
from . import views

urlpatterns = [
    path("request/", views.requestYouTubeDataAPI, name="requestYouTubeDataAPI"),
    path("", views.requestStaticDatabase, name="requestStaticDatabase"),
]
