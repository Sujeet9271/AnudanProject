# Generated by Django 3.2.4 on 2021-06-08 07:53

import anudaan.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Karyakram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='NagarPalika',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Samagri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('karyakram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samagri', to='anudaan.karyakram')),
                ('nagarpalika', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='anudaan.nagarpalika')),
            ],
            options={
                'ordering': ['karyakram'],
            },
        ),
        migrations.AddField(
            model_name='karyakram',
            name='nagarpalika',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='anudaan.nagarpalika'),
        ),
        migrations.CreateModel(
            name='AnudanPerosnal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ward', models.PositiveIntegerField(max_length=2)),
                ('Tole', models.CharField(max_length=255)),
                ('NagriktaNumber', models.PositiveBigIntegerField(max_length=12, verbose_name='Nagrikta Number')),
                ('JariJilla', models.CharField(max_length=20, verbose_name='Jaari Jilla')),
                ('NagriktaFront', models.ImageField(upload_to=anudaan.models.location, verbose_name='Nagrikta Front Photo')),
                ('NagriktaBack', models.ImageField(upload_to=anudaan.models.location, verbose_name='Nagrikta Back Photo')),
                ('approval', models.CharField(choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=14)),
                ('karyakram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anudaan.karyakram')),
                ('nagarpalika', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='anudaan.nagarpalika')),
                ('samagri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anudaan.samagri')),
            ],
        ),
        migrations.CreateModel(
            name='AnudanCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firm_name', models.CharField(max_length=255)),
                ('Pan_No', models.PositiveIntegerField(max_length=2)),
                ('Vat_No', models.CharField(max_length=255)),
                ('Registration_No', models.PositiveBigIntegerField(max_length=12, verbose_name='Registration Number')),
                ('ward', models.PositiveIntegerField(max_length=2)),
                ('Tole', models.CharField(max_length=255)),
                ('JariJilla', models.CharField(max_length=20, verbose_name='Jaari Jilla')),
                ('NagriktaFront', models.ImageField(upload_to=anudaan.models.location, verbose_name='Nagrikta Front Photo')),
                ('NagriktaBack', models.ImageField(upload_to=anudaan.models.location, verbose_name='Nagrikta Back Photo')),
                ('approval', models.CharField(choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=14)),
                ('karyakram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anudaan.karyakram')),
                ('nagarpalika', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='anudaan.nagarpalika')),
                ('samagri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anudaan.samagri')),
            ],
        ),
    ]
