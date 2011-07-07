from django.contrib.auth.models import User
from django.db import models
from organizations.models import Organization

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User)
    is_superuser = models.BooleanField()

class Database(models.Model):
    name = models.CharField(max_length=32)
    labs = models.ManyToManyField(Organization)
    contributors = models.ManyToManyField(Profile)

    def get_absolute_url(self):
        return reverse(
                'database_page', 
                kwargs = {
                    'slug': slugify(self.name) 
                })

class Repo(models.Model):
    path = models.CharField(max_length=255)
    files = models.ManyToManyField('File')
    database = models.ForeignKey(Database)
    device_type = models.CharField(max_length=1) 

    def get_absolute_url(self):
        return reverse(
                'repo_page',
                kwargs = {
                    'id': self.id,
                    'slug': slugify(self.name),
                    'device_type': self.device_type,}
                )

class Pulse_Sequence(models.Model):
    repo = models.ForeignKey(Repo)
    id_number = models.SmallIntegerField()

class File(models.Model):
    path = models.CharField(max_length=255)
    description = models.TextField()
    commit = models.ForeignKey('Commit')

class Commit(models.Model):
    timestamp = models.DateTimeField()
    githash = models.CharField(max_length=64) 
    user = models.ForeignKey(User)
    pulse_sequence = models.ForeignKey(Pulse_Sequence)
    files = models.ManyToManyField(File, related_name='ps')
    id_number = models.SmallIntegerField()
# need to make manual directory parameter
#    manual = models.FileField()

class ProfileToDb(models.Model):
    profile = models.ForeignKey(Profile)
    database = models.ForeignKey(Database)
    is_superuser = models.BooleanField()
