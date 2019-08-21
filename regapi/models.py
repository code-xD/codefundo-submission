from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.core.validators import URLValidator
# Create your models here.


class API(models.Model):
    api_name = models.CharField(max_length=255)
    api_key = models.PositiveIntegerField(primary_key=True, unique=True)
    api_secret = models.CharField(max_length=255)
    api_id = models.BigIntegerField(unique=True)
    callback_url = models.CharField(max_length=500, validators=[
                                    URLValidator()], null=True, blank=True)
    redirect_url = models.CharField(max_length=500, validators=[
                                    URLValidator()], null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.api_name)


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_id = models.BigIntegerField(primary_key=True, unique=True)
    api = models.ForeignKey(API, on_delete=models.CASCADE)
    private_key = models.CharField(max_length=500)

    def __str__(self):
        return str(self.event_name)


class Event_token(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.token)+'-'+str(self.event.event_id)


class Allowed_user(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.event_name+' '+self.user.username


class Login_Token(models.Model):
    token = models.CharField(max_length=50, unique=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Login_Token, self).save(*args, **kwargs)
        self.expiry_date += timedelta(minutes=15)
        super(Login_Token, self).save(*args, **kwargs)


class Name_list(models.Model):
    name_list = models.FileField(upload_to='name-list/')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
