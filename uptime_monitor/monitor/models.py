from django.db import models

# Create your models here.
class Site(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Check(models.Model):
    site = models.ForeignKey(Site,on_delete=models.CASCADE, related_name='checks')
    status = models.CharField(max_length=4)
    status_code = models.IntegerField(null=True,blank=True)
    response_time_ms = models.IntegerField(null=True, blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)
    error = models.CharField(max_length=200,blank=True)