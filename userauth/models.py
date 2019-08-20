from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
# Create your models here.


class OTP(models.Model):
    message = models.CharField(max_length=400)
    encrypt = models.CharField(max_length=400)
    private_key = models.CharField(max_length=400)
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(OTP, self).save(*args, **kwargs)
        self.expiry_date += timedelta(minutes=3)
        super(OTP, self).save(*args, **kwargs)
