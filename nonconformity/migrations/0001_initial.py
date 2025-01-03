# Generated by Django 5.1.2 on 2024-11-04 14:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NonConformity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(blank=True, choices=[('', 'No App Selected'), ('admin', 'Administration'), ('auth', 'Authentication and Authorization'), ('contenttypes', 'Content Types'), ('sessions', 'Sessions'), ('messages', 'Messages'), ('staticfiles', 'Static Files'), ('simple_history', 'Simple_History'), ('django_extensions', 'Django Extensions'), ('django_filters', 'Django_Filters'), ('rest_framework', 'Django REST framework'), ('accounts', 'Accounts'), ('locations', 'Locations'), ('inventory', 'Inventory'), ('maintenance', 'Maintenance'), ('methodology', 'Methodology'), ('analysis', 'Analysis'), ('nonconformity', 'Nonconformity')], max_length=100, verbose_name='Related App')),
                ('description', models.TextField(verbose_name='Description')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='nonconformity_photos/', verbose_name='Photo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
        ),
    ]
