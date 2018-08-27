# Generated by Django 2.1 on 2018-08-22 02:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0005_auto_20180819_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rssfeed',
            name='show_created',
        ),
        migrations.AddField(
            model_name='episode',
            name='publish_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]