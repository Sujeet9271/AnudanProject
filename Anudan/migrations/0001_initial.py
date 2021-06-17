# Generated by Django 3.2.4 on 2021-06-14 08:48

import Anudan.models
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
                ('name', models.CharField(help_text='Enter Samagri to Add', max_length=255)),
                ('karyakram', models.ForeignKey(help_text='Select Karyakram', on_delete=django.db.models.deletion.CASCADE, related_name='samagri', to='Anudan.karyakram')),
                ('nagarpalika', models.ForeignKey(help_text='Select Nagar Palika', on_delete=django.db.models.deletion.PROTECT, to='Anudan.nagarpalika')),
            ],
            options={
                'ordering': ['karyakram'],
            },
        ),
        migrations.AddField(
            model_name='karyakram',
            name='nagarpalika',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Anudan.nagarpalika'),
        ),
        migrations.CreateModel(
            name='AnudanPerosnal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ward', models.PositiveIntegerField(max_length=2)),
                ('tole', models.CharField(max_length=255)),
                ('nagrikta_number', models.PositiveBigIntegerField(max_length=12, verbose_name='Nagrikta Number')),
                ('jari_jilla', models.CharField(max_length=20, verbose_name='Jaari Jilla')),
                ('nagrikta_front', models.ImageField(upload_to=Anudan.models.personal_location, verbose_name='Nagrikta Front Photo')),
                ('nagrikta_back', models.ImageField(upload_to=Anudan.models.personal_location, verbose_name='Nagrikta Back Photo')),
                ('approval', models.CharField(choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=14)),
                ('karyakram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Anudan.karyakram')),
                ('nagarpalika', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Anudan.nagarpalika')),
                ('samagri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Anudan.samagri')),
            ],
        ),
        migrations.CreateModel(
            name='AnudanCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firm_name', models.CharField(max_length=255)),
                ('pan_no', models.PositiveIntegerField(max_length=2)),
                ('vat_no', models.CharField(max_length=255)),
                ('registration_no', models.PositiveBigIntegerField(max_length=12, verbose_name='Registration Number')),
                ('ward', models.PositiveIntegerField(max_length=2)),
                ('tole', models.CharField(max_length=255)),
                ('registered_place', models.CharField(max_length=20, verbose_name='Jaari Jilla')),
                ('firm_registration_proof', models.ImageField(upload_to=Anudan.models.company_location, verbose_name='Firm Registration Proof')),
                ('ward_sifaris', models.ImageField(upload_to=Anudan.models.company_location, verbose_name='Ward Sifaris')),
                ('prastavan', models.ImageField(upload_to=Anudan.models.company_location, verbose_name='Upload Prastavan')),
                ('approval', models.CharField(choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=14)),
                ('nagarpalika', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Anudan.nagarpalika')),
            ],
        ),
    ]