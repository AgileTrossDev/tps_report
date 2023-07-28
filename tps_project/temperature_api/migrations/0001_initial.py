# Generated by Django 3.2.20 on 2023-07-23 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TemperatureMeasurementModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('value', models.FloatField()),
            ],
            options={
                'db_table': 'temperature',
            },
        ),
    ]
