# Generated by Django 2.2.6 on 2020-01-27 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lpr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lprcamera_allowed_plates',
            name='allowed_plate',
            field=models.CharField(max_length=6),
        ),
    ]