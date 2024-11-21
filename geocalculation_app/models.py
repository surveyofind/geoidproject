from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    aadhar_no = models.CharField(max_length=100)
    aadharcard_upload = models.FileField(upload_to='image/', blank=True, null=True)
    nda_upload = models.FileField(upload_to='image/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    mobile_no = models.CharField(max_length=100,blank=True, null=True)
    govt_user = models.BooleanField('govt user', default=False)
    private_user = models.BooleanField('private user', default=False)
    academic_user = models.BooleanField('academic user', default=False) 
    institute_idcard = models.FileField(upload_to='image/', blank=True, null=True) 
    govt_idcard = models.FileField(upload_to='image/', blank=True, null=True)
    goverment_idcard_no = models.CharField(max_length=100, blank=True, null=True) 
    student_idcard_no = models.CharField(max_length=100, blank=True, null=True)
    user_types = models.CharField(max_length=100,blank=True, null=True)
    status = models.CharField(max_length=100,default='PENDING')
    

class GridData(models.Model):
    latitude_start = models.FloatField()
    latitude_end = models.FloatField()
    longitude_start = models.FloatField()
    longitude_end = models.FloatField()
    height_start = models.FloatField()
    height_end = models.FloatField()

class GridPoint(models.Model):
    grid_data = models.ForeignKey(GridData, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    state = models.CharField(max_length=500)
    value = models.CharField(max_length=500)



class databackup(models.Model):
    username = models.CharField(max_length=100,blank=True, null=True)
    user_type = models.CharField(max_length=100,blank=True, null=True)
    pointdownload = models.CharField(max_length=100,blank=True, null=True)
    updatetime = models.CharField(max_length=45, blank=True, null=True)