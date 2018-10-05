"""This module contains all urls and api endpoints"""

from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include([
        path("show/", views.ShowGetView.as_view(), name="api_show"),
        path("show/<int:pk>", views.SpecificShowGetView.as_view(),
             name="api_show_by_id"),
        path("show/<int:show_id>/<int:pk>",
             views.SpecificEpisodeGetView.as_view(),
             name="api_episode_by_show"),
        path("episode/", views.EpisodeGetView.as_view()),
        path("episode/<int:pk>",
             views.SpecificEpisodeGetView.as_view(),
             name="api_episode_by_id"),
    ])),
    path("cast/", views.cast, name="cast"),
    path("about/", views.about, name="about"),
    path("cast/<str:person_name>/", views.person_by_name, name="person"),
    path("<str:name>/", views.show_by_name, name="show by name"),
    path("<str:name>/<int:episode_number>/", views.episode_by_num,
         name="episode by number"),
    ]
