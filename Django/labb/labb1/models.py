from django.db import models
from django.utils.encoding import iri_to_uri
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

class Project(models.Model):
  name = models.CharField(max_length = 50)
  description = models.TextField()
  start_date = models.DateField()
  end_date = models.DateField()
  date_added = models.DateField()
  date_updated = models.DateField()
  user = models.ManyToManyField(User, related_name="projects")
  owner = models.ForeignKey(User, related_name="project")
  
  def owned_by_user(self, user):
    return self.owner == user

  def member_in_project(self, user):
    members = self.user.all()
    if user in members:
      return True
    else:
      return False

  def __unicode__(self):
    return self.name

  class Meta:
    permissions = (
      ("can_add_projects_web", "Can add projects"),
      )


class Status(models.Model):
  class Meta:
        verbose_name_plural = "status"
  status_name = models.CharField(max_length = 30)

  def __unicode__(self):
    return self.status_name

class Ticket(models.Model):
  name = models.CharField(max_length = 50)
  description = models.TextField()
  project = models.ForeignKey(Project, related_name="tickets")
  status = models.ForeignKey(Status, verbose_name="status", related_name="tickets")
  user = models.ForeignKey(User, related_name="tickets")
  date_added = models.DateField()
  date_updated = models.DateField()
  def __unicode__(self):
    return self.name

  def owned_by_user(self, user):
    return self.user == user

class ProjectForm(ModelForm):
  class Meta:
    model = Project
    exclude = ("owner", "date_added", "date_updated")

class LoginForm(forms.Form):
  username = forms.CharField(max_length = 30)
  password = forms.CharField(max_length = 30, widget = forms.PasswordInput)

class StatusForm(ModelForm):
  class Meta:
    model = Status

class TicketForm(ModelForm):
  class Meta:
    model = Ticket
    exclude = ("project", "user", "date_added", "date_updated")