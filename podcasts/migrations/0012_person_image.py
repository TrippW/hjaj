# Generated by Django 2.1 on 2018-08-23 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0011_auto_20180822_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='image',
            field=models.CharField(default='https://www.merriam-webster.com/assets/mw/images/article/art-wap-article-main/egg-3442-e1f6463624338504cd021bf23aef8441@1x.jpg', max_length=120),
        ),
    ]
