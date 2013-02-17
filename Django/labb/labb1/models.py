from django.db import models
from django.forms import ModelForm
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
  def __unicode__(self):
    return self.name

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

class ProjectForm(ModelForm):
  class Meta:
    model = Project

class StatusForm(ModelForm):
  class Meta:
    model = Status

class TicketForm(ModelForm):
  class Meta:
    model = Ticket