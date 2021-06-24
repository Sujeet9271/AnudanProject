# Generated by Django 3.2.4 on 2021-06-24 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0016_alter_palikauser_date_joined'),
        ('Anudan', '0011_alter_anudancompany_anya_darta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anudancompany',
            name='fiscal_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Accounts.fiscalyear', verbose_name='Fiscal Year'),
        ),
    ]