# Generated by Django 5.1 on 2024-12-09 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0006_remove_technician_adhaar_card_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='driving_license_photo',
            field=models.FileField(blank=True, null=True, upload_to='License'),
        ),
    ]
