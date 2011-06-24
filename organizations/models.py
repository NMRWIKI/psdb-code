from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

ACADEMIC = 0
INDUSTRIAL = 1
NON_PROFIT = 2
GOVERNMENT = 3
ORG_TYPE_CHOICES = (
    (ACADEMIC, 'academic lab'),
    (INDUSTRIAL, 'industrial'),
    (NON_PROFIT, 'non profit'),
    (GOVERNMENT, 'government'),
)
ORG_TYPE_URL2ID = (
    ('academic-labs', ACADEMIC),
    ('companies', INDUSTRIAL),
    ('non-profit-organizations', NON_PROFIT),
    ('government-organizations', GOVERNMENT),
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
    pi = models.ForeignKey(User, related_name = 'managed_organizations')
    name = models.CharField(max_length = 200, blank=True)
    description = models.TextField()
    url = models.URLField()
    org_type = models.SmallIntegerField(choices=ORG_TYPE_CHOICES)

    def save(self):
        if self.org_type == ACADEMIC and self.name == '':
            self.name = '%s Lab' % self.pi.username
        super(Organization, self).save()

    def get_absolute_url(self):
        return reverse(
            'org_page',
            kwargs = {'id': self.id, 'slug': slugify(self.name)}
            )

    def __unicode__(self):
        return self.name


class Appointment(models.Model):
    user = models.ForeignKey(User, related_name = 'appointments')
    organization = models.ForeignKey(
                                Organization,
                                related_name = 'appointments'
                            )
    title = models.SmallIntegerField(choices=TITLE_CHOICES)
    from_date = models.DateField(help_text = 'Enter dates as YYYY-MM-DD')
    to_date = models.DateField(null=True, blank=True, help_text = 'Leave blank if you are currently a member')

    def _get_status(self):
        return self.to_date == None

    def __unicode__(self):
        return '%s (%s, %s)' % (
            self.user.username,
            self.get_title_display(),
            self.organization.name,
        )

    is_active = property(_get_status)
