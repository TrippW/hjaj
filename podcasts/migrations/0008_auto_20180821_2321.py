# Generated by Django 2.1 on 2018-08-22 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0007_auto_20180821_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='publish_date',
            field=models.DateField(),
        ),
    ]
