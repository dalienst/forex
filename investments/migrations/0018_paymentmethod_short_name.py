# Generated by Django 4.2.7 on 2023-12-17 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0017_remove_package_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='short_name',
            field=models.CharField(default='Category', max_length=255),
        ),
    ]
