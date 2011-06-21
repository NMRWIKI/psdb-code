from django.forms import ModelForm
from organizations import models

class LabAccountForm(ModelForm):
    class Meta:
        model = models.Organization
        fields = ('pi', 'description', 'url',)
