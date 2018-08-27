from django.contrib import admin

from .models import RSSFeed, Show, Episode, Log, Person

admin.site.register(RSSFeed)
admin.site.register(Show)
admin.site.register(Episode)
admin.site.register(Log)
admin.site.register(Person)
