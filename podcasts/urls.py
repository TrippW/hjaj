from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('cast/', views.cast, name='cast'),
    path('about/', views.about, name='about'),  
    path('cast/<str:person_name>/', views.person_by_name, name='person'),
    path('<str:name>/', views.show_by_name, name='show by name'),
    path('<str:name>/<int:episode_number>/', views.episode_by_num, name='episode by number'),

    ]
