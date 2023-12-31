# Generated by Django 4.2.7 on 2023-12-13 20:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investments', '0006_investcategory_daily_usdt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Package',
                'verbose_name_plural': 'Packages',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('detail', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.PositiveIntegerField(blank=True, null=True)),
                ('wallet', models.CharField(blank=True, max_length=1000, null=True)),
                ('till_number', models.PositiveIntegerField(blank=True, null=True)),
                ('paybill', models.PositiveIntegerField(blank=True, null=True)),
                ('account', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Payment Method',
                'verbose_name_plural': 'Payment Methods',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='investcategory',
            options={'ordering': ['-created_at'], 'verbose_name': 'Investment Category', 'verbose_name_plural': 'Investment Categories'},
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('amount', models.PositiveIntegerField()),
                ('phone', models.PositiveIntegerField()),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawals', to='investments.package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('amount', models.PositiveIntegerField()),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], max_length=10)),
                ('phone', models.PositiveIntegerField()),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='investments.package')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='package',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investments.investcategory'),
        ),
        migrations.AddField(
            model_name='package',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investments.paymentmethod'),
        ),
        migrations.AddField(
            model_name='package',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('amount', models.PositiveIntegerField()),
                ('phone', models.PositiveIntegerField()),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits', to='investments.package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
