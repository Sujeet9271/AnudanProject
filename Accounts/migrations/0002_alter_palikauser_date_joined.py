# Generated by Django 3.2.4 on 2021-06-24 14:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palikauser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2021, 6, 24, 14, 21, 0, 925534, tzinfo=utc), verbose_name='date joined'),
        ),
    ]
