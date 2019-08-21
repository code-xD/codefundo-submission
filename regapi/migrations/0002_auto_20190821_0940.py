# Generated by Django 2.2.4 on 2019-08-21 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api',
            name='api_id',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='api',
            name='api_key',
            field=models.BigIntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.BigIntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]