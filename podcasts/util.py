"""This module is holds the utility functions for processing and updating
the website. Only the update function should be called from outside of the
module. Handles converting RSS to JSON data, checking the timing between
updates, and adding new shows and episodes.
"""

import calendar
import json
import traceback
from datetime import timedelta
from xml.etree.ElementTree import fromstring
import requests
from django.utils import timezone
from xmljson import BadgerFish as bf
from .models import Episode, Show, RSSFeed, Log


def get_podcast_data(url):
    """Converts rss feed to json data

    args: url
    url is an rss url

    returns: json formatted data
    """
    result = requests.get(url)
    j = json.dumps(bf().data(fromstring(result.content)))
    decoded = json.JSONDecoder().decode(j)
    data = decoded["rss"]["channel"]
    return data


def add_new_log(title, description=""):
    """Used to add a log to the database

    args: title, [description]
    title is the name that will be apparent when browsing the log
    description is optional to supply more details to the log
    """
    Log(title=title, description=description).save()


def save_image(img_name, img_data):
    """save an image to the website

    args: img_name img_data
    img_name is the path to where the image will be saved (stemming from
        the static path)
    img_data is the data recieved from the website request
    """
    with open("podcasts/static/"+img_name, 'wb') as handler:
        handler.write(img_data)


def add_episode(show_id, item, title):
    """Add episode data to db and website"""
    description = item["description"]['$']
    url = item["{http://search.yahoo.com/mrss/}content"]["@url"]
    pub_data = item["pubDate"]['$']
    pub_data = pub_data.split(' ')
    month = list(calendar.month_abbr).index(pub_data[2])

    publish_date = "{2:04d}-{0:02d}-{1:02d}"
    publish_date = publish_date.format(int(month), int(pub_data[1]),
                                       int(pub_data[3]))

    episode = Episode(show=show_id, publish_date=publish_date,
                      title=title, description=description,
                      audio_url=url)
    episode.save()

    title = "Added New Episode"
    description = "Added episode '{:s}' to the show '{:s}'."
    description = description.format(episode.title, show_id.name)

    add_new_log(title, description)

    return episode


def add_show(data, rss):
    """Adds show data provided by rss feed to db and website"""
    #get data from rss for show
    title = data["title"]["$"]
    short_name = "".join([rss[0].upper() for rss in title.split(' ')])
    desc = data["{http://www.itunes.com/dtds/podcast-1.0.dtd}summary"]['$']

    #Save image and image path
    img = data["{http://www.itunes.com/dtds/podcast-1.0.dtd}image"]["@href"]
    img_data = requests.get(img).content
    img_name = "podcasts/imgs/" + short_name + "_logo.jpg"
    save_image(img_name, img_data)

    #create and save the show
    new_show = Show(rss=rss, name=title, description=desc, image=img,
                    short_name=short_name)
    new_show.save()

    title = "Added New Show"
    description = "Added the new show {:s} to the roster.".format(title)
    add_new_log(title, description)

    return new_show




def check_last_update(hours=0, minutes=5):
    """Checks if a feed update should be proccessed. Returns True if an update
    should continue, or False if it should be halted.

    If an update was started within the last 30 seconds or completed within
    a provided amount of time, prevents multiple updates
    from happening at once and lessens the load on the server if there is
    high traffic
    """
    last_update_completed = Log.objects.filter(title="Completed Feed Update")
    last_update_started = Log.objects.filter(title="Start Feed Update")


    if last_update_started.count() > 0:
        #an update has been started before, so we should check if its been
        #30 seconds since the last attempt
        last_start_time = last_update_started.latest("time").time
        start_time_buffer = last_start_time + timedelta(seconds=30)

        if start_time_buffer > timezone.now():
            #it has not been 30 seconds yet, do not update
            return False


        if last_update_completed.count() > 0:
            last_complete_time = last_update_completed.latest("time").time
            complete_time_buffer = last_complete_time \
                                   + timedelta(minutes=minutes, hours=hours)

            if complete_time_buffer > timezone.now():
                return False
    #no updates have been started or no updates have been completed or no
    #updates have
    return True


def check_episodes(items, rss):
    """Check for and add missing episodes to specified show"""
    episode_list = Episode.objects.filter(show__name=rss.name)
    all_episode_titles = [k.title for k in episode_list]

    for item in items:
        title = item["title"]["$"]
        if title not in all_episode_titles:
            show_id = Show.objects.get(name=rss.name)
            add_episode(show_id, item, title)



def check_all_feeds():
    """Checks each feed and adds the necessary data and episodes"""
    for rss in RSSFeed.objects.all():
        data = get_podcast_data(rss.rss_url)

        #add the show if it is missing (This will happen if the
        #RSS feed was just added or the show was deleted
        #Also update the name of the RSS feed to match the name of the show
        if rss.name not in [k.name for k in Show.objects.all()]:
            add_show(data, rss)


            rss.name = data["title"]['$']
            rss.save()

        check_episodes(data["item"], rss)



def update(minutes_between_updates=30):
    """Checks and updates the database based on rss feed if it hasn't
    successfully updated within n time. This process begins the site update
    """
    if check_last_update(minutes=minutes_between_updates):
        add_new_log("Start Feed Update")
        try:
            check_all_feeds()
            add_new_log("Completed Feed Update")
        except:
            title = "Failed Feed Update"
            description = traceback.format_exc()
            add_new_log(title, description)
