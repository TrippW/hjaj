from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .util import update
from .models import Show, Episode, Person
from django.template import loader

def verify_get(query_set, error="Something went wrong"):
    if len(query_set) == 0:
        raise Http404(error)
    else:
        return query_set[0]

def index(request):
    update()
    show_list = Show.objects.all()
    template = loader.get_template('podcasts/index.html')
    context = {
        'show_list' : show_list,
    }
    return HttpResponse(template.render(context, request))

def show(request, show_id):
    update()
    show = verify_get(Show.objects.filter(id = show_id), "Unknown Show")
    episode_list = Episode.objects.filter(show__id = show_id).order_by('-publish_date','-title')
    template = loader.get_template('podcasts/show.html')
    context = {
        'episode_list' : episode_list,
        'show' : show,
    }
    return HttpResponse(template.render(context, request))

def show_by_name(request, name):
    show_id = verify_get(Show.objects.filter(short_name=name), "Unknown Show").id
    
    return show(request, show_id)

def episode_by_num(request, name, episode_number):
    show_id = verify_get(Show.objects.filter(short_name=name), "Unknown Show").id

    ordered_episodes = Episode.objects.all().filter(show__id = show_id).order_by('publish_date','title')
    if episode_number <= 0 or episode_number > len(ordered_episodes) :
        raise Http404("Episode does not exist")
    ep_id = ordered_episodes[episode_number-1].id
    return episode(request, show_id, ep_id)

def episode(request, show_id, episode_id):
    update()
    episode = verify_get(Episode.objects.filter(id = episode_id), "Unknown Episode")
    show = verify_get(Show.objects.filter(id = show_id), "Unknown Show")
                      
    template = loader.get_template('podcasts/episode.html')
    context = {
        'episode' : episode,
        'show' : show,
    }
    return HttpResponse(template.render(context, request))

def cast(request):
    cast = Person.objects.all()
    template = loader.get_template('podcasts/cast.html')
    context = {
        'cast' : cast
    }
    return HttpResponse(template.render(context, request))

def person_by_name(request, person_name):
    person_name = person_name.replace("_", " ")
    person_id = Person.objects.filter(name=person_name)[0].id
    return person(request, person_id)

def person(request, person_id):
    person = verify_get(Person.objects.filter(id=person_id), "Unknown Person")
    template = loader.get_template('podcasts/person.html')
    context = {
        'person' : person,
    }
    return HttpResponse(template.render(context, request))


def about(request):
    template=loader.get_template('podcasts/about.html')
    return HttpResponse(template.render(None, request))
