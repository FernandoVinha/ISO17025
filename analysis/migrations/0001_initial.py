# Generated by Django 5.1.2 on 2024-11-02 18:51

import django.db.models.deletion
import django.utils.timezone
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('methodology', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_type', models.CharField(help_text='Type of analysis performed', max_length=255)),
                ('conformity', models.BooleanField(default=True, help_text='Indicates if the analysis is compliant with expected results')),
                ('analyzed_at', models.DateTimeField(auto_now_add=True)),
                ('results', models.JSONField(help_text='Analysis results in JSON format')),
                ('approval_date', models.DateTimeField(blank=True, null=True)),
                ('analyzed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analyzed_items', to=settings.AUTH_USER_MODEL)),
                ('approved_by', models.ForeignKey(blank=True, default=None, help_text='User who approved the analysis', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_analyses', to=settings.AUTH_USER_MODEL)),
                ('methodology', models.ForeignKey(help_text='Methodology used for the analysis', on_delete=django.db.models.deletion.CASCADE, related_name='analyses', to='methodology.methodology')),
            ],
            options={
                'verbose_name': 'Analysis',
                'verbose_name_plural': 'Analyses',
                'permissions': [('can_view_analysis', 'Can view analyses'), ('can_add_analysis', 'Can add analyses'), ('can_change_analysis', 'Can change analyses'), ('can_delete_analysis', 'Can delete analyses')],
            },
        ),
        migrations.CreateModel(
            name='AnalysisApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_date', models.DateTimeField(auto_now_add=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected')], max_length=50)),
                ('analysis', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='approval', to='analysis.analysis')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approvals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_view_analysisapproval', 'Can view analysis approvals'), ('can_add_analysisapproval', 'Can add analysis approvals'), ('can_change_analysisapproval', 'Can change analysis approvals'), ('can_delete_analysisapproval', 'Can delete analysis approvals')],
            },
        ),
        migrations.CreateModel(
            name='AnalysisRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the analysis request', max_length=255)),
                ('comments', models.TextField(blank=True, help_text='Additional instructions or comments from the client', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the analysis request was created')),
                ('sample_image', models.ImageField(blank=True, help_text='Image of the sample related to the request', null=True, upload_to='request_images/')),
                ('methodologies', models.ManyToManyField(help_text='Methodologies to be applied to the samples', related_name='analysis_requests', to='methodology.methodology')),
                ('requested_by', models.ForeignKey(blank=True, help_text='User (client) who made the analysis request', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analysis_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Analysis Request',
                'verbose_name_plural': 'Analysis Requests',
                'permissions': [('can_view_analysisrequest', 'Can view analysis requests'), ('can_add_analysisrequest', 'Can add analysis requests'), ('can_change_analysisrequest', 'Can change analysis requests'), ('can_delete_analysisrequest', 'Can delete analysis requests')],
            },
        ),
        migrations.CreateModel(
            name='HistoricalAnalysisRequest',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the analysis request', max_length=255)),
                ('comments', models.TextField(blank=True, help_text='Additional instructions or comments from the client', null=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False, help_text='Date and time when the analysis request was created')),
                ('sample_image', models.TextField(blank=True, help_text='Image of the sample related to the request', max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('requested_by', models.ForeignKey(blank=True, db_constraint=False, help_text='User (client) who made the analysis request', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Analysis Request',
                'verbose_name_plural': 'historical Analysis Requests',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalReceptionItem',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the received item', max_length=255)),
                ('serial_number', models.CharField(blank=True, db_index=True, help_text='Serial number of the item', max_length=100, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, help_text='Weight of the item', max_digits=10, null=True)),
                ('received_at', models.DateTimeField(blank=True, editable=False)),
                ('condition', models.CharField(help_text='Condition of the item upon reception', max_length=255)),
                ('sample_image', models.TextField(blank=True, help_text='Image of the received sample', max_length=100, null=True)),
                ('shipment_date', models.DateField(blank=True, help_text='Date of shipment', null=True)),
                ('shipment_location', models.CharField(blank=True, help_text='Location of shipment', max_length=255, null=True)),
                ('max_days_for_result', models.IntegerField(blank=True, help_text='Maximum number of days for the result', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('analysis_request', models.ForeignKey(blank=True, db_constraint=False, help_text='Analysis request associated with the item', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='analysis.analysisrequest')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('received_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Reception Item',
                'verbose_name_plural': 'historical Reception Items',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='ReceptionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the received item', max_length=255)),
                ('serial_number', models.CharField(blank=True, help_text='Serial number of the item', max_length=100, null=True, unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, help_text='Weight of the item', max_digits=10, null=True)),
                ('received_at', models.DateTimeField(auto_now_add=True)),
                ('condition', models.CharField(help_text='Condition of the item upon reception', max_length=255)),
                ('sample_image', models.ImageField(blank=True, help_text='Image of the received sample', null=True, upload_to='reception_images/')),
                ('shipment_date', models.DateField(blank=True, help_text='Date of shipment', null=True)),
                ('shipment_location', models.CharField(blank=True, help_text='Location of shipment', max_length=255, null=True)),
                ('max_days_for_result', models.IntegerField(blank=True, help_text='Maximum number of days for the result', null=True)),
                ('analysis_request', models.ForeignKey(help_text='Analysis request associated with the item', on_delete=django.db.models.deletion.CASCADE, related_name='reception_items', to='analysis.analysisrequest')),
                ('received_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reception Item',
                'verbose_name_plural': 'Reception Items',
                'permissions': [('can_view_receptionitem', 'Can view reception items'), ('can_add_receptionitem', 'Can add reception items'), ('can_change_receptionitem', 'Can change reception items'), ('can_delete_receptionitem', 'Can delete reception items')],
            },
        ),
        migrations.CreateModel(
            name='HistoricalDisposal',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('disposal_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('reason', models.TextField()),
                ('comments', models.TextField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('analysis', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='analysis.analysis')),
                ('disposed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='analysis.receptionitem')),
            ],
            options={
                'verbose_name': 'historical Disposal',
                'verbose_name_plural': 'historical Disposals',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalAnalysis',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('analysis_type', models.CharField(help_text='Type of analysis performed', max_length=255)),
                ('conformity', models.BooleanField(default=True, help_text='Indicates if the analysis is compliant with expected results')),
                ('analyzed_at', models.DateTimeField(blank=True, editable=False)),
                ('results', models.JSONField(help_text='Analysis results in JSON format')),
                ('approval_date', models.DateTimeField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('analyzed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('approved_by', models.ForeignKey(blank=True, db_constraint=False, default=None, help_text='User who approved the analysis', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('methodology', models.ForeignKey(blank=True, db_constraint=False, help_text='Methodology used for the analysis', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='methodology.methodology')),
                ('item', models.ForeignKey(blank=True, db_constraint=False, help_text='Reception item being analyzed', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='analysis.receptionitem')),
            ],
            options={
                'verbose_name': 'historical Analysis',
                'verbose_name_plural': 'historical Analyses',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Disposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disposal_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('reason', models.TextField()),
                ('comments', models.TextField(blank=True, null=True)),
                ('analysis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='disposal_records', to='analysis.analysis')),
                ('disposed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='disposed_items', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disposals', to='analysis.receptionitem')),
            ],
            options={
                'verbose_name': 'Disposal',
                'verbose_name_plural': 'Disposals',
                'permissions': [('can_view_disposal', 'Can view disposals'), ('can_add_disposal', 'Can add disposals'), ('can_change_disposal', 'Can change disposals'), ('can_delete_disposal', 'Can delete disposals')],
            },
        ),
        migrations.AddField(
            model_name='analysis',
            name='item',
            field=models.ForeignKey(help_text='Reception item being analyzed', on_delete=django.db.models.deletion.CASCADE, related_name='analysis_records', to='analysis.receptionitem'),
        ),
    ]
