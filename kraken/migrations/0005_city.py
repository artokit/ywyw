# Generated by Django 4.1.6 on 2023-03-01 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kraken', '0004_userdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
