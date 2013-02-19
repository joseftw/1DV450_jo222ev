from django import template

register = template.Library()

@register.filter(name = 'creator')
def creator(project, user):
  return project.owner == user

@register.filter(name = 'member')
def member(project, user):
  import pdb; pdb.set_trace()
  users = project.user
  print users
  if user in users: 
    return True
  return False

@register.filter(name = 'ticketCreator')
def ticketCreator(ticket, user):
  return ticket.user == user