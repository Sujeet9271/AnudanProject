# Generated by Django 3.2.4 on 2021-06-24 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Anudan', '0015_anudancompany_fiscal_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='anudancompany',
            name='anya_darta',
            field=models.CharField(blank=True, choices=[('Gharelu', 'Gharelu'), ('Vanijya', 'Vanijya')], max_length=50, null=True),
        ),
    ]
