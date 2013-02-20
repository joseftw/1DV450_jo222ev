from django import template

register = template.Library()

@register.filter(name = 'creator')
def creator(project, user):
  return project.owner == user

@register.filter(name = 'member')
def member(project, user):
  members = project.user
  if user in members: 
    return True
  return False

@register.filter(name = 'ticketCreator')
def ticketCreator(ticket, user):
  return ticket.user == user