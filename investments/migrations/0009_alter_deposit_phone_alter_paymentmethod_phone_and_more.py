# Generated by Django 4.2.7 on 2023-12-13 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0008_alter_deposit_phone_alter_paymentmethod_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='phone',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='phone',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='withdrawal',
            name='phone',
            field=models.BigIntegerField(),
        ),
    ]
