from django.shortcuts import get_list_or_404, render, get_object_or_404, render, redirect
from labb1.models import Project, Ticket, Status, ProjectForm, LoginForm, User, TicketForm
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def login_user(request):
  
  if(request.method == "POST"):

    form = LoginForm(request.POST)
    if form.is_valid():
      username_to_try = form.cleaned_data["username"]
      password_to_try = form.cleaned_data["password"]

      user = authenticate(username = username_to_try, password = password_to_try)
     
      if user is not None:
        if user.is_active:
          login(request, user)
          messages.success(request, 'Welcome ' + request.user.first_name)
          request.session["isLoggedIn"] = True
          request.session["user_id"] = user.id
          request.session["user"] = User.objects.get(id = user.id)
          return redirect("project_list")
        else:
          return HttpResponse("<h1>Your account is disabled</h1>")
      else:
        messages.error(request, 'Wrong username and/or password ')
  else:
    form = LoginForm()
  return render(request, "login/login.html", {'form' : form})

def logout_user(request):
  logout(request)
  messages.info(request, 'You have logged out')
  request.session["isLoggedIn"] = False
  return redirect('home')

@login_required
def project_list(request):
    projects = Project.objects.order_by('date_updated')
    user = request.user
    # Gets all critical tickets
    tickets = Ticket.objects.filter(status__status_name = "Critical")
    return render(request, 'projects/list.html', {"projects" : projects, "tickets" : tickets, "user" : user})

@login_required
def project_add(request):
    if request.method == "POST":
      form = ProjectForm(request.POST)
      if form.is_valid():
        form.instance.date_added = datetime.date.today()
        form.instance.date_updated = datetime.date.today()
        form.instance.owner = request.user
        try:
          form.save()
          messages.success(request, 'Successfully added the "' + form.instance.name + '" project!')
          return redirect("project_list")
        except:
          return HttpResponseServerError()
    else:
        form = ProjectForm()
    return render(request, 'projects/add.html', {"form" : form})
    return HttpResponse('Permission denied')

@login_required
def project_delete(request, project_id):
  user = request.user
  project = get_object_or_404(Project, pk=project_id)
  if project.owned_by_user(request.user): 
    name = project.name
    project.delete()
    messages.success(request, 'The project "' + name + '" has been deleted.')
    return redirect ('project_list')
  else:
    messages.error(request, 'You have no permission to delete the "' + project.name + '" project.')
    return render(request, 'projects/show.html', {"project" : project})

@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owned_by_user(request.user):
      if(request.method == "POST"):
        form = ProjectForm(request.POST, instance = project)
        if form.is_valid():
          try:
            form.save()
            messages.success(request, 'You have successfully edited the "' + project.name + '" project!')
            url = reverse('project_show', kwargs={'project_id': project.id})
            return HttpResponseRedirect(url)
          except:
            return HttpResponseServerError()
      else:
        form = ProjectForm(instance = project)
      return render(request, 'projects/edit.html', {"form" : form, "project" : project})
    else:
      messages.error(request, 'You have no permission to edit the "'+ project.name +'" project.')
      return render(request, 'projects/show.html', {"project" : project})

@login_required
def project_show(request, project_id):
    project = Project.objects.get(id=project_id)
    members = project.user
    tickets = project.tickets   
    return render(request, 'projects/show.html', {"project" : project, "members" : members, "tickets" : tickets})

@login_required
def project_show_tickets(request, project_id):
    project = Project.objects.get(id=project_id) 
    tickets = Project.objects.get(id=project_id).tickets.all()
    return render(request, 'projects/show_project_tickets.html', {"project" : project, "tickets" : tickets})

@login_required
def project_join(request, project_id):
    project = Project.objects.get(id = project_id)
    user = request.user
    if not project.member_in_project(user):
      project.user.add(user)
      project.save
      messages.success(request, 'You have joined the project "' + project.name + '"!')
      url = reverse('project_show', kwargs={'project_id': project.id})
      return HttpResponseRedirect(url)
    else:
      messages.info(request, 'You are already a member of the "' + project.name + '" project.')
      url = reverse('project_show', kwargs={'project_id': project.id})
      return HttpResponseRedirect(url)

@login_required
def ticket_show(request, project_id, ticket_id):
    project = Project.objects.get(id=project_id)
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'tickets/show.html', {"project" : project, "ticket" : ticket})

@login_required
def ticket_edit(request, project_id, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    project = get_object_or_404(Project, pk = project_id)
    if project.owned_by_user(request.user) or ticket.owned_by_user(request.user):
      if(request.method == "POST"):
        form = TicketForm(request.POST, instance = ticket)
        if form.is_valid():
          form.instance.date_added = datetime.date.today()
          form.instance.date_updated = datetime.date.today()
          form.instance.user = User.objects.get(id = request.session["user_id"])
          form.instance.project = project
          try:
            form.save()
            messages.success(request, 'You have successfully edited the ticket "' + ticket.name + '"!')
            url = reverse('project_show', kwargs={'project_id': project.id})
            return HttpResponseRedirect(url)
          except:
            return HttpResponseServerError()
      else:
        form = TicketForm(instance = ticket)
      return render(request, 'tickets/edit.html', {"form" : form, "ticket" : ticket, "project" : project})
    else:
      messages.error(request, 'You have no permission to edit the "' + ticket.name + '" ticket.')
      return render(request, 'tickets/show.html', {"project" : project, "ticket" : ticket})

@login_required
def project_delete_ticket(request, project_id, ticket_id):
    project = get_object_or_404(Project, pk = project_id)
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    name = ticket.name
    if project.owned_by_user(request.user) or ticket.owned_by_user(request.user):
      ticket.delete();
      messages.success(request, 'You have successfully removed the ticket "' + name +'"!')
      url = reverse('project_show', kwargs={'project_id': project.id})
      return HttpResponseRedirect(url)
    else:
      messages.error(request, 'You have no permission to remove the ticket "' + name + '".')
      url = reverse('project_show', kwargs={'project_id': project.id})
      return HttpResponseRedirect(url)

@login_required
def project_add_ticket(request, project_id):
    user = request.user
    project = Project.objects.get(id = project_id)
    if project.owned_by_user(user) or project.member_in_project(user): 
      if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
          form.instance.date_added = datetime.date.today()
          form.instance.date_updated = datetime.date.today()
          form.instance.user = User.objects.get(id = request.session["user_id"])
          form.instance.project = Project.objects.get(id = project_id)
          try:
            form.save()
            messages.success(request, 'You have successfully added a ticket for the "' + project.name + '"" project!')
            tickets = project.tickets
            url = reverse('project_show', kwargs={'project_id': project.id})
            return HttpResponseRedirect(url)
          except:
            return HttpResponseServerError()
      else:
          form = TicketForm()
      return render(request, 'tickets/add.html', {"form" : form, "project" : project})
      return HttpResponse('Permission denied')
    else:
      messages.info(request, 'You have no permission to add a ticket, you need to be a member of the "' + project.name + '" project.')
      url = reverse('project_show', kwargs={'project_id': project.id})
      return HttpResponseRedirect(url)

def home(request):
  return render(request, "home/index.html")