from django.forms import ModelForm
from organizations import models

class LabAccountForm(ModelForm):
    class Meta:
        model = models.Organization
        fields = ('name', 'pi', 'org_type', 'description', 'url', )
