# Generated by Django 2.2.4 on 2019-08-19 19:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='API',
            fields=[
                ('api_name', models.CharField(max_length=255)),
                ('api_key', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('api_secret', models.CharField(max_length=255)),
                ('api_id', models.IntegerField(unique=True)),
                ('callback_url', models.CharField(blank=True, max_length=500, null=True, validators=[django.core.validators.URLValidator()])),
                ('redirect_url', models.CharField(blank=True, max_length=500, null=True, validators=[django.core.validators.URLValidator()])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_name', models.CharField(max_length=255)),
                ('event_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('private_key', models.CharField(max_length=500)),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regapi.API')),
            ],
        ),
        migrations.CreateModel(
            name='Name_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_list', models.FileField(upload_to='name-list/')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regapi.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Login_Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=50, unique=True)),
                ('expiry_date', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regapi.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Event_token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(max_length=50, unique=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regapi.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Allowed_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regapi.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
