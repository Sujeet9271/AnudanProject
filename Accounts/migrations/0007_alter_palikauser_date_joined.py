# Generated by Django 3.2.4 on 2021-06-17 05:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0006_alter_palikauser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palikauser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2021, 6, 17, 5, 53, 4, 665090, tzinfo=utc)),
        ),
    ]