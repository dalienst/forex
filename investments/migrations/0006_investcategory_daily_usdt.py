# Generated by Django 4.2.7 on 2023-12-13 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0005_investcategory_daily_withdrawal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='investcategory',
            name='daily_usdt',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
