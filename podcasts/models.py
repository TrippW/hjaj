from django.db import models

class RSSFeed(models.Model):
    name = models.CharField(max_length=50)
    rss_url = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Show(models.Model):
    rss = models.ForeignKey(RSSFeed, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=120)
    twitter = models.CharField(max_length=150, blank=True, null=True)
    facebook = models.CharField(max_length=150, blank=True, null=True)
    tumblr = models.CharField(max_length=150, blank=True, null=True)
    short_name = models.CharField(max_length=25, blank=True, null=True,
                                  default=None)

    def __str__(self):
        return self.name

class Log(models.Model):
    title = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, default=None, blank=True,
                                   null=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{} | {}".format(self.title, self.time)

class Episode(models.Model):
    show = models.ForeignKey(Show, related_name='episode_ids', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    audio_url = models.CharField(max_length=80)
    publish_date = models.DateField()

    def __str__(self):
        return self.title

class ShowRating(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    rater_name = models.CharField(max_length=50, default="guest")
    text = models.CharField(max_length=500)


    def __str__(self):
        return self.text[:30]

class EpisodeRating(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    rater_name = models.CharField(max_length=50, default="guest")
    text = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.text[:30]

class Person(models.Model):
    default_img_url = "https://www.merriam-webster.com/assets/mw/images/" \
                      + "article/art-wap-article-main/egg-3442-e1f646362" \
                      + "4338504cd021bf23aef8441@1x.jpg"
    name = models.CharField(max_length=75)
    twitter = models.CharField(max_length=150, blank=True, null=True)
    tumblr = models.CharField(max_length=150, blank=True, null=True)
    image = models.CharField(max_length=150, default=default_img_url)
    email = models.CharField(max_length=150, blank=True, null=True)
    personal_web = models.CharField(max_length=150, blank=True, null=True)
    about = models.CharField(max_length=500, blank=True, null=True)
    shows = models.ManyToManyField(Show)

    def has_shows(self):
        return len(self.shows.all()) != 0

    def get_url_name(self):
        return self.name.replace(" ", "_")

    def __str__(self):
        return self.name
