# Generated by Django 3.1.4 on 2021-03-27 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210327_1914'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chatmessage',
            unique_together=set(),
        ),
    ]