# Generated by Django 3.2.4 on 2021-06-15 08:47

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('Anudan', '0004_auto_20210614_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anudanperosnal',
            name='karyakram',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='nagarpalika', chained_model_field='nagarpalika', on_delete=django.db.models.deletion.PROTECT, to='Anudan.karyakram'),
        ),
        migrations.AlterField(
            model_name='anudanperosnal',
            name='samagri',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='karyakram', chained_model_field='karyakram', on_delete=django.db.models.deletion.PROTECT, to='Anudan.samagri'),
        ),
        migrations.AlterField(
            model_name='samagri',
            name='karyakram',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='nagarpalika', chained_model_field='nagarpalika', on_delete=django.db.models.deletion.PROTECT, to='Anudan.karyakram'),
        ),
    ]
