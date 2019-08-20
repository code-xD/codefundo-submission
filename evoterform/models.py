from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
# Image size 1200x750(max)


class AccountDetail(models.Model):
    aadhar_no = models.BigIntegerField(unique=True, primary_key=True)
    email = models.EmailField()
    govtID_card = models.ImageField(upload_to='ID/')
    address_proof = models.ImageField(upload_to='Address_Proof/')
    voter_photo = models.ImageField(upload_to='Passport_Photo/')
    connectionHash = models.CharField(max_length=255, null=True, blank=True)
    voterID = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "Cache "+str(self.aadhar_no)

    def save(self):
        super().save()
        imgg = Image.open(self.govtID_card.path)
        imga = Image.open(self.address_proof.path)
        imgv = Image.open(self.voter_photo.path)
        output_size = (300, 300)
        imgv.resize(output_size, Image.ANTIALIAS)
        imgv.save(self.voter_photo.path)
        output_size = (400, 244)
        imgg.resize(output_size, Image.ANTIALIAS)
        imgg.save(self.govtID_card.path)
        output_size = (500, 707)
        imga.resize(output_size, Image.ANTIALIAS)
        imga.save(self.address_proof.path)


class CacheVoterData(models.Model):
    voter_name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.IntegerField()
    aadhar_no = models.IntegerField(primary_key=True, unique=True)
    aLine1 = models.CharField(max_length=500)
    aLine2 = models.CharField(max_length=500)
    s_code = models.IntegerField()
    c_code = models.IntegerField()
    d_code = models.IntegerField()
    pin = models.IntegerField()

    def __str__(self):
        return "Cache Data "+str(self.aadhar_no)


class WorkerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    task_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username+' Profile'


class Task(models.Model):
    connectionurl = models.CharField(max_length=500, null=True, blank=True)
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE)
    connectionHash = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.worker.user.username+'-'+str(self.id)
