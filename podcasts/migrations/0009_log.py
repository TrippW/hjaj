# Generated by Django 2.1 on 2018-08-22 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0008_auto_20180821_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]