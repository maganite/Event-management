# Generated by Django 4.2.11 on 2024-04-11 07:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userdetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Latitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('Longitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('Date', models.DateField(default=datetime.date.today)),
            ],
        ),
    ]