# Generated by Django 2.1 on 2018-08-19 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RSS_feeds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rss_url', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='show',
            name='rss_url',
        ),
    ]
