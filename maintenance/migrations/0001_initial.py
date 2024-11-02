# Generated by Django 5.1.2 on 2024-10-26 22:08

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CalibrationStandard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('last_calibration_date', models.DateField(help_text='Last calibration date of the standard')),
                ('certification_body', models.CharField(help_text='Certification organization', max_length=255)),
                ('acceptable_error_margin', models.DecimalField(decimal_places=5, help_text='Acceptable error margin for the equipment', max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='StandardOperatingProcedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('document', models.FileField(help_text='Standard Operating Procedure (SOP) document', upload_to='sops/')),
                ('description', models.TextField(blank=True, help_text='SOP description', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Verification date and time')),
                ('measurements', models.JSONField(help_text='Measurements taken by the user')),
                ('user', models.ForeignKey(help_text='User who performed the verification', on_delete=django.db.models.deletion.CASCADE, related_name='daily_verifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Daily Verification',
                'verbose_name_plural': 'Daily Verifications',
                'permissions': [('can_view_dailyverification', 'Can view daily verifications'), ('can_add_dailyverification', 'Can add daily verifications'), ('can_change_dailyverification', 'Can change daily verifications'), ('can_delete_dailyverification', 'Can delete daily verifications')],
            },
        ),
        migrations.CreateModel(
            name='HistoricalTraining',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('training_name', models.CharField(help_text='Training name', max_length=255)),
                ('date_completed', models.DateField(help_text='Training completion date')),
                ('certification_document', models.TextField(blank=True, help_text='Certification document', max_length=100, null=True)),
                ('description', models.TextField(blank=True, help_text='Description of the training or acquired skills', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('contact', models.ForeignKey(blank=True, db_constraint=False, help_text='Technician who received the training', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounts.contacts')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Training',
                'verbose_name_plural': 'historical Trainings',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency_months', models.PositiveIntegerField(help_text='Maintenance interval in months')),
                ('last_maintenance_date', models.DateField(blank=True, help_text='Last maintenance date', null=True)),
                ('description', models.TextField(blank=True, help_text='Description of maintenance work', null=True)),
                ('report', models.FileField(blank=True, help_text='Maintenance report', null=True, upload_to='maintenance_reports/')),
                ('item', models.ForeignKey(help_text='Item to be maintained', on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_records', to='inventory.inventoryitem')),
                ('technician', models.ForeignKey(blank=True, help_text='Technician responsible for maintenance', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenance_tasks', to='accounts.contacts')),
                ('sop', models.ForeignKey(blank=True, help_text='SOP followed during maintenance', null=True, on_delete=django.db.models.deletion.SET_NULL, to='maintenance.standardoperatingprocedure')),
            ],
            options={
                'verbose_name': 'Maintenance',
                'verbose_name_plural': 'Maintenances',
                'permissions': [('can_view_maintenance', 'Can view maintenances'), ('can_add_maintenance', 'Can add maintenances'), ('can_change_maintenance', 'Can change maintenances'), ('can_delete_maintenance', 'Can delete maintenances')],
            },
        ),
        migrations.CreateModel(
            name='HistoricalMaintenance',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('frequency_months', models.PositiveIntegerField(help_text='Maintenance interval in months')),
                ('last_maintenance_date', models.DateField(blank=True, help_text='Last maintenance date', null=True)),
                ('description', models.TextField(blank=True, help_text='Description of maintenance work', null=True)),
                ('report', models.TextField(blank=True, help_text='Maintenance report', max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(blank=True, db_constraint=False, help_text='Item to be maintained', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.inventoryitem')),
                ('technician', models.ForeignKey(blank=True, db_constraint=False, help_text='Technician responsible for maintenance', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounts.contacts')),
                ('sop', models.ForeignKey(blank=True, db_constraint=False, help_text='SOP followed during maintenance', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='maintenance.standardoperatingprocedure')),
            ],
            options={
                'verbose_name': 'historical Maintenance',
                'verbose_name_plural': 'historical Maintenances',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCalibration',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('frequency_months', models.PositiveIntegerField(help_text='Calibration interval in months')),
                ('last_calibration_date', models.DateField(blank=True, help_text='Last calibration date', null=True)),
                ('measurement_uncertainty', models.DecimalField(blank=True, decimal_places=5, help_text='Associated measurement uncertainty', max_digits=10, null=True)),
                ('description', models.TextField(blank=True, help_text='Description of calibration work', null=True)),
                ('report', models.TextField(blank=True, help_text='Calibration report', max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(blank=True, db_constraint=False, help_text='Item to be calibrated', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.inventoryitem')),
                ('standard', models.ForeignKey(blank=True, db_constraint=False, help_text='Calibration standard used for traceability', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='maintenance.calibrationstandard')),
                ('technician', models.ForeignKey(blank=True, db_constraint=False, help_text='Technician responsible for calibration', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounts.contacts')),
                ('sop', models.ForeignKey(blank=True, db_constraint=False, help_text='SOP followed during calibration', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='maintenance.standardoperatingprocedure')),
            ],
            options={
                'verbose_name': 'historical Calibration',
                'verbose_name_plural': 'historical Calibrations',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Calibration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency_months', models.PositiveIntegerField(help_text='Calibration interval in months')),
                ('last_calibration_date', models.DateField(blank=True, help_text='Last calibration date', null=True)),
                ('measurement_uncertainty', models.DecimalField(blank=True, decimal_places=5, help_text='Associated measurement uncertainty', max_digits=10, null=True)),
                ('description', models.TextField(blank=True, help_text='Description of calibration work', null=True)),
                ('report', models.FileField(blank=True, help_text='Calibration report', null=True, upload_to='calibration_reports/')),
                ('item', models.ForeignKey(help_text='Item to be calibrated', on_delete=django.db.models.deletion.CASCADE, related_name='calibration_records', to='inventory.inventoryitem')),
                ('technician', models.ForeignKey(blank=True, help_text='Technician responsible for calibration', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='calibration_tasks', to='accounts.contacts')),
                ('standard', models.ForeignKey(blank=True, help_text='Calibration standard used for traceability', null=True, on_delete=django.db.models.deletion.SET_NULL, to='maintenance.calibrationstandard')),
                ('sop', models.ForeignKey(blank=True, help_text='SOP followed during calibration', null=True, on_delete=django.db.models.deletion.SET_NULL, to='maintenance.standardoperatingprocedure')),
            ],
            options={
                'verbose_name': 'Calibration',
                'verbose_name_plural': 'Calibrations',
                'permissions': [('can_view_calibration', 'Can view calibrations'), ('can_add_calibration', 'Can add calibrations'), ('can_change_calibration', 'Can change calibrations'), ('can_delete_calibration', 'Can delete calibrations')],
            },
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_name', models.CharField(help_text='Training name', max_length=255)),
                ('date_completed', models.DateField(help_text='Training completion date')),
                ('certification_document', models.FileField(blank=True, help_text='Certification document', null=True, upload_to='certifications/')),
                ('description', models.TextField(blank=True, help_text='Description of the training or acquired skills', null=True)),
                ('contact', models.ForeignKey(help_text='Technician who received the training', on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to='accounts.contacts')),
            ],
            options={
                'verbose_name': 'Training',
                'verbose_name_plural': 'Trainings',
                'permissions': [('can_view_training', 'Can view trainings'), ('can_add_training', 'Can add trainings'), ('can_change_training', 'Can change trainings'), ('can_delete_training', 'Can delete trainings')],
            },
        ),
    ]
