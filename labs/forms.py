from django.forms import ModelForm
from labs import models

class LabAccountForm(ModelForm):
    class Meta:
        model = models.LabAccount
        fields = ('members', 'pi', 'description', 'url',)
