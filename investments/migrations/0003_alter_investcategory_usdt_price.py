# Generated by Django 4.2.7 on 2023-12-13 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0002_investcategory_max_price_investcategory_usdt_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investcategory',
            name='usdt_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]