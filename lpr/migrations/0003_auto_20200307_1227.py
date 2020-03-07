# Generated by Django 2.2.6 on 2020-03-07 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lpr', '0002_auto_20200127_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='lprcamera',
            name='eth_gateway',
            field=models.CharField(default='192.168.1.1', max_length=16),
        ),
        migrations.AddField(
            model_name='lprcamera',
            name='eth_ip',
            field=models.CharField(default='192.168.1.10', max_length=16),
        ),
        migrations.AddField(
            model_name='lprcamera',
            name='eth_mask',
            field=models.PositiveIntegerField(default=24),
        ),
    ]
