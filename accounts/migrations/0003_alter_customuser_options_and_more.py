# Generated by Django 5.1.2 on 2024-11-15 20:43

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_historicalcontacts_company_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('can_generate_invite', 'Can generate invitation link')], 'verbose_name': 'Custom User', 'verbose_name_plural': 'Custom Users'},
        ),
        migrations.AlterModelOptions(
            name='historicalrelationshiptype',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Relationship Type', 'verbose_name_plural': 'historical Relationship Types'},
        ),
        migrations.AlterModelOptions(
            name='invitation',
            options={'verbose_name': 'Invitation', 'verbose_name_plural': 'Invitations'},
        ),
        migrations.AlterModelOptions(
            name='relationshiptype',
            options={'permissions': [('create_relationshiptype', 'Can create relationship type'), ('edit_relationshiptype', 'Can edit relationship type')], 'verbose_name': 'Relationship Type', 'verbose_name_plural': 'Relationship Types'},
        ),
        migrations.AddField(
            model_name='invitation',
            name='role',
            field=models.CharField(choices=[('client', 'Client'), ('supplier', 'Supplier'), ('maintenance', 'Maintenance'), ('employee', 'Employee')], default='client', max_length=20, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Joined'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Is Staff'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='user_profiles/', verbose_name='Profile Image'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('client', 'Client'), ('supplier', 'Supplier'), ('maintenance', 'Maintenance'), ('employee', 'Employee')], default='employee', max_length=20, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='historicalrelationshiptype',
            name='name',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='token',
            field=models.CharField(blank=True, max_length=32, unique=True, verbose_name='Token'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='used',
            field=models.BooleanField(default=False, verbose_name='Used'),
        ),
        migrations.AlterField(
            model_name='relationshiptype',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Name'),
        ),
        migrations.CreateModel(
            name='HistoricalCustomUser',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=254, verbose_name='Email Address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Last Name')),
                ('role', models.CharField(choices=[('client', 'Client'), ('supplier', 'Supplier'), ('maintenance', 'Maintenance'), ('employee', 'Employee')], default='employee', max_length=20, verbose_name='Role')),
                ('profile_image', models.TextField(blank=True, max_length=100, null=True, verbose_name='Profile Image')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is Staff')),
                ('date_joined', models.DateTimeField(blank=True, editable=False, verbose_name='Date Joined')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Custom User',
                'verbose_name_plural': 'historical Custom Users',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalInvitation',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=254, verbose_name='Email Address')),
                ('token', models.CharField(blank=True, db_index=True, max_length=32, verbose_name='Token')),
                ('role', models.CharField(choices=[('client', 'Client'), ('supplier', 'Supplier'), ('maintenance', 'Maintenance'), ('employee', 'Employee')], default='client', max_length=20, verbose_name='Role')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Created At')),
                ('used', models.BooleanField(default=False, verbose_name='Used')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Invitation',
                'verbose_name_plural': 'historical Invitations',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
