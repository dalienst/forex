# Generated by Django 4.2.7 on 2023-12-17 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0012_remove_deposit_trans_ref_deposit_package_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposit',
            name='user',
        ),
    ]
