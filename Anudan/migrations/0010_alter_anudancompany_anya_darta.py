# Generated by Django 3.2.4 on 2021-06-24 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Anudan', '0009_alter_anudancompany_anya_darta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anudancompany',
            name='anya_darta',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
