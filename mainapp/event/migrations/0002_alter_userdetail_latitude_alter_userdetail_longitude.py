# Generated by Django 4.2.11 on 2024-04-11 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='Latitude',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='Longitude',
            field=models.CharField(max_length=15),
        ),
    ]
