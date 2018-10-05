"""This module contains all unit tests for the application"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.reverse import reverse
from .models import RSSFeed, Show, Episode

def create_test_rss(self):
    """Create a basic rss feed for testing"""
    self.rss_name = "fake rss feed"
    self.rss_url = "fake url"
    self.rss = RSSFeed(name=self.rss_name, rss_url=self.rss_url)
    return self.rss

def create_test_show(self):
    """Create a basic show for testing"""
    self.show_name = "Test Show"
    self.show_description = "This is a fake show for testing."
    self.image = "/podcasts/fake.png"
    self.show = Show(rss=self.rss, name=self.show_name,
                     description=self.show_description, image=self.image)
    return self.show

def create_test_episode(self):
    """Create a basic episode for testing"""
    self.episode_title = "Test Episode"
    self.episode_description = "This is a fake episode for testing."
    self.episode_audio_url = "\fake_location\fakeaudio.mp4"
    self.episode_publish_date = "1999-12-31"
    self.episode = Episode(show=self.show, title=self.episode_title,
                           description=self.episode_description,
                           audio_url=self.episode_audio_url,
                           publish_date=self.episode_publish_date)
    return self.episode

class RSSFeedTestCase(TestCase):
    """This class will test the RSSFeed model."""

    def setUp(self):
        """Define the test client and other variables"""
        self.rss = create_test_rss(self)

    def test_model_can_create_rss_feed(self):
        """test that the rssFeed module can create an rss feed"""
        old_count = RSSFeed.objects.count()
        self.rss.save()
        new_count = RSSFeed.objects.count()
        self.assertNotEqual(old_count, new_count)


class ShowTestCase(TestCase):
    """This class will test the Show model."""

    def setUp(self):
        """Defeine the test client and other test variables."""
        create_test_rss(self).save()
        self.show = create_test_show(self)

    def test_model_can_create_show(self):
        """Test that the show module can create a show"""
        old_count = Show.objects.count()
        self.show.save()
        new_count = Show.objects.count()
        self.assertNotEqual(old_count, new_count)

class EpisodeTestCase(TestCase):
    """This class will test the Episode model."""
    def setUp(self):
        """Defeine the test client and other test variables."""
        create_test_rss(self).save()
        create_test_show(self).save()
        self.episode = create_test_episode(self)

    def test_model_can_create_episode(self):
        """Test that the show module can create a show"""
        old_count = Episode.objects.count()
        self.episode.save()
        new_count = Episode.objects.count()
        self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Defeine the test client and other test variables."""
        self.client = APIClient()

    def test_all_shows_empty(self):
        """Test that API responds from endpoint"""
        url = reverse("api_show")
        json_response = self.client.get(url, format='json')
        self.assertEqual(json_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response.content), 2)

    def test_all_shows_result(self):
        """Test that api returns a show when there is at least one show available."""
        create_test_rss(self).save()
        create_test_show(self).save()
        url = reverse("api_show")
        json_response = self.client.get(url, format='json')
        self.assertEqual(json_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(json_response.content), 2)

    def test_all_shows_multiple(self):
        """Verify that api will list a number of shows"""
        create_test_rss(self).save()
        create_test_show(self).save()
        url = reverse("api_show")
        json_response = self.client.get(url, format='json')
        old_count = len(json_response.content)
        create_test_rss(self).save()
        create_test_show(self).save()
        json_response = self.client.get(url, format='json')
        new_count = len(json_response.content)
        self.assertNotEqual(old_count, new_count)

    def test_show_displays_episodes(self):
        """Verify that api will list episodes for a show"""
        create_test_rss(self).save()
        create_test_show(self).save()
        url = reverse("api_show")
        json_response = self.client.get(url, format='json')
        old_count = len(json_response.content)
        create_test_episode(self).save()
        json_response = self.client.get(url, format='json')
        new_count = len(json_response.content)
        self.assertNotEqual(old_count, new_count)
