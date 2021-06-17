# Generated by Django 3.2.4 on 2021-06-14 14:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('Anudan', '0003_alter_samagri_karyakram'),
    ]

    operations = [
        migrations.AddField(
            model_name='karyakram',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='karyakram',
            name='update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='anudanperosnal',
            name='karyakram',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='nagarpalika', chained_model_field='nagarpalika', on_delete=django.db.models.deletion.PROTECT, to='Anudan.karyakram'),
        ),
        migrations.AlterField(
            model_name='anudanperosnal',
            name='samagri',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='karyakram', chained_model_field='karyakram', on_delete=django.db.models.deletion.PROTECT, to='Anudan.samagri'),
        ),
        migrations.AlterField(
            model_name='samagri',
            name='karyakram',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='nagarpalika', chained_model_field='nagarpalika', on_delete=django.db.models.deletion.PROTECT, to='Anudan.karyakram'),
        ),
    ]