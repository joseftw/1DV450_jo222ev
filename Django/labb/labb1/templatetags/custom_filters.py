from django import template

register = template.Library()

@register.filter(name = 'creator')
def creator(project, user):
  return project.owner == user

@register.filter(name = 'member')
def member(project, user):
  members = project.user.all()
  if user in members: 
    return True
  return False

@register.filter(name = 'ticketCreator')
def ticketCreator(ticket, user):
  return ticket.user == user

@register.filter(name = 'isLoggedIn')
def isLoggedIn():
  if request.session["isLoggedIn"]:
    return True
  else:
    return False