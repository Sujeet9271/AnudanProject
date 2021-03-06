# Generated by Django 3.2.4 on 2021-06-26 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Municipality', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='FiscalYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'verbose_name': 'Fiscal Year',
                'verbose_name_plural': 'Fiscal Year',
                'db_table': 'Fiscal_Year',
            },
        ),
        migrations.CreateModel(
            name='PalikaUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is staff')),
                ('is_admin', models.BooleanField(default=False, verbose_name='is admin')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='is superuser')),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='address')),
                ('contact_number', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='contact number')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Profile', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profile',
                'db_table': 'Profile',
            },
        ),
        migrations.CreateModel(
            name='MunicipalityStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipality_staff', to='Municipality.municipality', verbose_name='Municipality')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='municipality_staff', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'staff',
                'verbose_name_plural': 'staffs',
                'db_table': 'Staff',
            },
        ),
    ]
