# Generated by Django 4.2.11 on 2024-04-11 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_eventdata_date_alter_eventdata_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdata',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
