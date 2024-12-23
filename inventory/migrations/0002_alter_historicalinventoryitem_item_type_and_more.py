# Generated by Django 5.1.2 on 2024-10-26 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinventoryitem',
            name='item_type',
            field=models.CharField(choices=[('SIMPLE', 'Simple Item'), ('SUPPLY', 'Supply'), ('TOOL', 'Tool'), ('MEASURING', 'Measuring Equipment'), ('ELECTRONIC', 'Electronic Equipment'), ('MACHINE', 'Machine'), ('FURNITURE', 'Furniture'), ('OTHER', 'Other')], max_length=10),
        ),
        migrations.AlterField(
            model_name='historicalinventoryitem',
            name='unit',
            field=models.CharField(blank=True, choices=[('L', 'Liters'), ('G', 'Grams'), ('U', 'Unit')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='item_type',
            field=models.CharField(choices=[('SIMPLE', 'Simple Item'), ('SUPPLY', 'Supply'), ('TOOL', 'Tool'), ('MEASURING', 'Measuring Equipment'), ('ELECTRONIC', 'Electronic Equipment'), ('MACHINE', 'Machine'), ('FURNITURE', 'Furniture'), ('OTHER', 'Other')], max_length=10),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='unit',
            field=models.CharField(blank=True, choices=[('L', 'Liters'), ('G', 'Grams'), ('U', 'Unit')], max_length=2, null=True),
        ),
    ]
