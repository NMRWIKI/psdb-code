from django.db import models
from django.contrib.auth.models import User

ACADEMIC = 0
INDUSTRIAL = 1
NON_PROFIT = 2
GOVERNMENT = 3
ORG_TYPE_CHOICES = (
    (ACADEMIC, 'academic'),
    (INDUSTRIAL, 'industrial'),
    (NON_PROFIT, 'non-profit'),
    (GOVERNMENT, 'government'),
)

PROFESSOR = 0
UNDERGRAD = 1
GRAD_STUDENT = 2
POST_DOC = 3
ACADEMIC_STAFF = 4
ENGINEER = 5
SALESPERSON = 6
IND_MANAGER = 7
IND_ENGINEER = 8
IND_SCIENTIST = 9

TITLE_CHOICES = (
    (PROFESSOR, 'professor'),
    (UNDERGRAD, 'undergraduate student'),
    (GRAD_STUDENT, 'graduate student'),
    (POST_DOC, 'postdoc'),
    (ACADEMIC_STAFF, 'academic staff' ),
    (ENGINEER, 'engineer'),
    (SALESPERSON, 'salesperson'),
    (IND_MANAGER, 'industrial manager'),
    (IND_ENGINEER, 'industrial engineer'),
    (IND_SCIENTIST, 'industrial scientist'),
)
# Create your models here.
class Organization(models.Model):
    pi = models.ForeignKey(User, related_name = 'managed_labs')
    name = models.CharField(max_length = 200, help_text='help')
    description = models.TextField()
    url = models.URLField()
    org_type = models.SmallIntegerField(choices=ORG_TYPE_CHOICES)

    def save(self):
        if self.org_type == ACADEMIC and self.name is None:
            self.org_type = '%s lab' % self.pi.username
        super(Organization, self).save()


class Appointment(models.Model):
    user = models.ForeignKey(User, related_name = 'organizations')
    organization = models.ForeignKey(
                                Organization,
                                related_name = 'appointments'
                            )
    title = models.SmallIntegerField(choices=TITLE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField(null=True)

    def _get_status(self):
        return self.to_date == None

    is_active = property(_get_status)
