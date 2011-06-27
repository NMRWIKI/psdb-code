from django.forms import ModelForm
from organizations import models

class OrganizationForm(ModelForm):
    class Meta:
        model = models.Organization
        fields = ('name', 'org_type', 'description', 'url', )

class AppointmentForm(ModelForm):
    class Meta:
        model = models.Appointment
        fields = ('title', 'from_date', 'to_date', )
