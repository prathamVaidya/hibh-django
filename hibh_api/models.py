from django.db import models

# Create your models here.

class Tracker(models.Model):
    email= models.CharField(max_length=255)
    is_email_verified= models.BooleanField(default=False)
    name= models.CharField(max_length=255)
    email_token= models.CharField(max_length=255)
    public_key= models.CharField(max_length=255, unique=True)
    private_key= models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Alert(models.Model):
    tracker_id= models.ForeignKey(Tracker, on_delete=models.CASCADE)
    ip_address= models.CharField(max_length=255)
    useragent= models.CharField(max_length=255)
    country= models.CharField(max_length=255)
    country_flag= models.CharField(max_length=255)
    region= models.CharField(max_length=255)
    city= models.CharField(max_length=255)
    coordinates= models.CharField(max_length=255)
    zip_code= models.CharField(max_length=255)
    isp= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)