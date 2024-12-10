# Generated by Django 5.1 on 2024-12-09 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0007_alter_driver_driving_license_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='technician',
            name='adhaar_card_photo',
            field=models.FileField(blank=True, null=True, upload_to='Documents'),
        ),
        migrations.AddField(
            model_name='technician',
            name='others',
            field=models.FileField(blank=True, null=True, upload_to='Documents'),
        ),
        migrations.AddField(
            model_name='technician',
            name='profile_photo',
            field=models.FileField(blank=True, null=True, upload_to='Documents'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='adhaar_card_photo',
            field=models.FileField(blank=True, null=True, upload_to='Documents'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='driving_license_photo',
            field=models.FileField(blank=True, null=True, upload_to='Documents'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='profile_photo',
            field=models.FileField(blank=True, null=True, upload_to='Documents'),
        ),
    ]