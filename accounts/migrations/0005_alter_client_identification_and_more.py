# Generated by Django 4.2.7 on 2023-12-13 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_client_identification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='identification',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
