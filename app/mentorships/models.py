from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from lib.utils import shorten_url
from accounts.models import Skill


class Project(models.Model):
    PROJECT_TYPE_CHOICES = (
            ('m', 'Mentoring'),
            ('l', 'Looking for Mentors')
        )
    added_by = models.ForeignKey(User)
    skills = models.ManyToManyField(Skill)
    description = models.TextField(max_length=1000)
    title = models.CharField(max_length=120)
    looking_for = models.TextField(max_length=1000)
    project_type = models.CharField(max_length=1, choices=PROJECT_TYPE_CHOICES, default="l")
    members = models.ManyToManyField(User, null=True, blank=True, related_name="members")
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return self.title
    
    @property
    def share_url(self):
        url = settings.SERVER_SCHEME_AND_NETLOC + '/support/' + str(self.id)
        return shorten_url(url)

class JoinRequest(models.Model):
    added_by = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    note = models.TextField(max_length=1000)
    closed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.project.title
 
class ProjectLog(models.Model):
    '''Describes progress of an established mentorship'''
    project = models.ForeignKey(Project)
    content = models.TextField(max_length=1000)
    added_by = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return self.mentorship.from_user.first_name

class Sponsor(models.Model):
    project = models.ForeignKey(Project)
    email = models.EmailField()
    receive_email_updates = models.BooleanField(default=True)

    def __unicode__(self):
        return self.mentorship_request.from_user.first_name


