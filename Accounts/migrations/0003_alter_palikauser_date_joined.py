# Generated by Django 3.2.4 on 2021-06-20 07:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_auto_20210620_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palikauser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2021, 6, 20, 7, 53, 44, 800509, tzinfo=utc)),
        ),
    ]
