# Generated by Django 5.1 on 2024-12-09 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0008_technician_adhaar_card_photo_technician_others_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='technician',
            old_name='others',
            new_name='other_docs',
        ),
    ]
