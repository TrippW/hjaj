"""This module contains all views for all webpages"""

from django.http import HttpResponse, Http404
from django.template import loader
from rest_framework import generics
from .util import update
from .serializers import ShowSerializer, EpisodeSerializer
from .models import Show, Episode, Person

def verify_get(query_set, error="Something went wrong"):
    """Verifies that the query was successful,
       otherwise displays 404 error
       """
    if query_set.exists():
        return query_set[0]
    raise Http404(error)

class ShowGetView(generics.ListAPIView):
    """This class defines the get behavior to list all shows"""
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

class EpisodeGetView(generics.ListAPIView):
    """This class defines the get behavior to list all episodes"""
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer

class SpecificShowGetView(generics.RetrieveAPIView):
    """This class defines the get behavior to list a specific Show"""
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

class SpecificEpisodeGetView(generics.RetrieveAPIView):
    """This class defines the get behavior to list all episodes"""
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer


def index(request):
    """display's all shows"""
    update()
    show_list = Show.objects.all()
    template = loader.get_template("podcasts/index.html")
    context = {
        "show_list" : show_list,
    }
    return HttpResponse(template.render(context, request))

def show(request, show_id):
    """display's a specific show's episodes"""
    update()
    show_obj = verify_get(Show.objects.filter(id=show_id), \
                          "Unknown Show")
    episodes = Episode.objects.filter(show__id=show_id)
    episode_list = episodes.order_by("-publish_date", "-title")
    template = loader.get_template("podcasts/show.html")
    context = {
        "episode_list" : episode_list,
        "show" : show_obj,
    }
    return HttpResponse(template.render(context, request))

def show_by_name(request, name):
    """display's a specific show's episodes"""
    show_id = verify_get(Show.objects.filter(short_name=name), \
                         "Unknown Show").id

    return show(request, show_id)

def episode_by_num(request, name, episode_number):
    """display's a page for a specific episode"""
    show_id = verify_get(Show.objects.filter(short_name=name), \
                          "Unknown Show").id
    episodes = Episode.objects.all()
    filtered_episodes = episodes.filter(show__id=show_id)
    ordered_episodes = filtered_episodes.order_by("publish_date", \
                                                  "title")
    if episode_number <= 0 or episode_number > len(ordered_episodes):
        raise Http404("Episode does not exist")
    ep_id = ordered_episodes[episode_number-1].id
    return episode(request, show_id, ep_id)

def episode(request, show_id, episode_id):
    """display's a page for a specific episode"""
    update()
    episode_obj = verify_get(Episode.objects.filter(id=episode_id), \
                                                "Unknown Episode")
    show_obj = verify_get(Show.objects.filter(id=show_id), \
                          "Unknown Show")

    template = loader.get_template("podcasts/episode.html")
    context = {
        "episode" : episode_obj,
        "show" : show_obj,
    }
    return HttpResponse(template.render(context, request))

def cast(request):
    """display's a page of all people involved"""
    cast_obj = Person.objects.all()
    template = loader.get_template("podcasts/cast.html")
    context = {
        "cast" : cast_obj
    }
    return HttpResponse(template.render(context, request))

def person_by_name(request, person_name):
    """display's a specific person's page"""
    person_name = person_name.replace('_', ' ')
    person_id = Person.objects.filter(name=person_name)[0].id
    return person(request, person_id)

def person(request, person_id):
    """displays a specific person's papge"""
    person_obj = verify_get(Person.objects.filter(id=person_id), \
                            "Unknown Person")
    template = loader.get_template("podcasts/person.html")
    context = {
        "person" : person_obj,
    }
    return HttpResponse(template.render(context, request))


def about(request):
    """displays the about page"""
    template = loader.get_template("podcasts/about.html")
    return HttpResponse(template.render(None, request))
