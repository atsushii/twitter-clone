# Generated by Django 3.1.4 on 2021-03-28 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210328_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweetretweetaction',
            name='retweet',
        ),
        migrations.RemoveField(
            model_name='tweetretweetaction',
            name='tweet',
        ),
        migrations.DeleteModel(
            name='TweetLikeAction',
        ),
        migrations.DeleteModel(
            name='TweetRetweetAction',
        ),
    ]