# Generated by Django 3.2.4 on 2021-06-24 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0019_alter_palikauser_date_joined'),
        ('Anudan', '0014_auto_20210624_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='anudancompany',
            name='fiscal_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='Accounts.fiscalyear', verbose_name='Fiscal Year'),
        ),
    ]
