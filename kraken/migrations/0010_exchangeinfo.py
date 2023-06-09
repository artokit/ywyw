# Generated by Django 4.1.6 on 2023-03-22 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kraken', '0009_exchange_card_exchange_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeInfo',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False)),
                ('random_number', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField()),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kraken.exchange')),
            ],
        ),
    ]
