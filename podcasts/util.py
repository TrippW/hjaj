from .models import Episode, Show, RSSFeed, Log
import requests
import os
import json
from xmljson import BadgerFish as bf
from xml.etree.ElementTree import fromstring
import calendar
from django.utils import timezone
from datetime import timedelta
import traceback

def get_podcast_data(url):
    result = requests.get(url)
    j = json.dumps(bf().data(fromstring(result.content)))
    decoded = json.JSONDecoder().decode(j)
    data = decoded['rss']['channel']
    return data

def add_episode(show_id, item, title):
    description = item['description']['$']
    url = item["{http://search.yahoo.com/mrss/}content"]['@url']
    pub_data = item['pubDate']['$']
    pub_data = pub_data.split(" ")
    month = list(calendar.month_abbr).index(pub_data[2])
    
    publish_date = "{2:04d}-{0:02d}-{1:02d}".format(int(month), int(pub_data[1]), int(pub_data[3]))

    episode = Episode(show = show_id, publish_date=publish_date, title = title, description = description, audio_url = url)
    episode.save()
    Log(title="Added New Episode", description="Added episode '{:s}' to the show '{:s}'.".format(episode.title,show_id.name)).save()
    return episode

def add_show(data):
    title = data["title"]['$']
    short_name= "".join([i[0].upper() for i in title.split(" ")])
    desc=data["{http://www.itunes.com/dtds/podcast-1.0.dtd}summary"]['$']
    img=data["{http://www.itunes.com/dtds/podcast-1.0.dtd}image"]['@href']
    img_data = requests.get(img).content
    img="podcasts/imgs/"+short_name+"_logo.jpg"
    with open("podcasts/static/"+img, 'wb') as handler:
        handler.write(img_data)
    new_show = Show(rss = i, name = title, description=desc, image=img, short_name=short_name)
    new_show.save()
    Log(title="Added New Show", description="Added the new show {:s} to the roster.".format(title)).save()
    return new_show

def update():
    last_update = Log.objects.filter(title="Completed Feed Update")
    #if last_update:
        #if timezone.now() < (last_update.latest('time').time + timedelta(minutes=5)):
            #return "Skip"
                            
    Log(title="Start Feed Update").save()
    try:
        for i in RSSFeed.objects.all():
            data = get_podcast_data(i.rss_url)
            if i.name not in [k.name for k in Show.objects.all()]:
                #add the show if it is missing (This will happen if the RSS feed was just added or the show was deleted
                add_show(data)

                #update the name of the RSS feed to match the name of the show
                i.name = data["title"]['$']
                i.save()

            all_episode_titles = [k.title for k in Episode.objects.filter(show__name = i.name)]
            
            for item in data['item']:
                title = item['title']['$']
                if title not in all_episode_titles:
                    show_id = Show.objects.get(name = i.name)
                    add_episode(show_id, item, title)
        Log(title="Completed Feed Update").save()
    except:
        Log(title="Failed Feed Update", description=traceback.format_exc()).save()
    return "Complete"
