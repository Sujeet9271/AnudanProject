# Generated by Django 3.2.4 on 2021-06-24 08:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0013_alter_palikauser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palikauser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2021, 6, 24, 8, 34, 40, 205557, tzinfo=utc), verbose_name='date joined'),
        ),
    ]
