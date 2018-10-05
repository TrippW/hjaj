"""This class contains all serializers to change models into JSON data"""

from rest_framework import serializers
from .models import Show, Episode

class ShowSerializer(serializers.ModelSerializer):
    """Serailizer to map Show instance into JSON format."""
    episode_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with Show fields"""
        model = Show
        fields = ('id', 'name', 'description', 'image', 'twitter', \
                  'facebook', 'tumblr', 'short_name', 'episode_ids')
        read_only_fields = ('name', 'description', 'image', 'twitter', \
                            'facebook', 'tumblr', 'short_name')

class EpisodeSerializer(serializers.ModelSerializer):
    """Serailizer to map Episode instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with Episode fields"""
        model = Episode
        fields = ('id', 'title', 'description', 'audio_url', 'publish_date')
        read_only_fields = ('title', 'description', 'audio_url', \
                            'publish_date')
