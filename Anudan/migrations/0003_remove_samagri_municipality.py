# Generated by Django 3.2.4 on 2021-06-23 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Anudan', '0002_alter_samagri_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='samagri',
            name='municipality',
        ),
    ]
