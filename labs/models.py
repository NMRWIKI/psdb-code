from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LabAccount(models.Model):
    pi = models.ForeignKey(User, related_name = 'managed_labs')
    name = models.CharField(max_length = 200, blank=True, help_text='help')
    members = models.ManyToManyField(User, related_name = 'labs')
    description = models.TextField()
    url = models.URLField()
