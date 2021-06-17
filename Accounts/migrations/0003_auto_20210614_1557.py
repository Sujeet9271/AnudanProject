# Generated by Django 3.2.4 on 2021-06-14 10:12

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_alter_palikauser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palikastaff',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='palika_staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='palikauser',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2021, 6, 14, 10, 12, 46, 346603, tzinfo=utc)),
        ),
    ]