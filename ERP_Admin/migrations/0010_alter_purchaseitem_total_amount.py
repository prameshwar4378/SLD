# Generated by Django 5.1 on 2024-12-10 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Admin', '0009_rename_others_technician_other_docs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
