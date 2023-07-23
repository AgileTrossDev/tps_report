# Generated by Django 4.2.3 on 2023-07-22 07:21

from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(unique=True)),
                ('value', models.FloatField()),
                ('timezone', timezone_field.fields.TimeZoneField(default='UTC')),
            ],
        ),
    ]
