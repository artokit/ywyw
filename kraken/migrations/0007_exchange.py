# Generated by Django 4.1.6 on 2023-03-20 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kraken', '0006_userdata_city_selected'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('exchange_rate', models.FloatField()),
                ('count', models.FloatField()),
                ('min_exchange', models.FloatField()),
                ('commission', models.FloatField()),
            ],
        ),
    ]
