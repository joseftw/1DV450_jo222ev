from django.shortcuts import get_list_or_404, render, get_object_or_404, render, redirect
from labb1.models import Project, Ticket, Status, ProjectForm, LoginForm
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse

def login_user(request):
  message = ''
  if(request.method == "POST"):

    form = LoginForm(request.POST)
    if form.is_valid():
      username_to_try = form.cleaned_data["username"]
      password_to_try = form.cleaned_data["password"]

      user = authenticate(username = username_to_try, password = password_to_try)
     
      if user is not None:
        if user.is_active:
          login(request, user)
          message = "Welcome" + user.first_name
          request.session["user_id"] = user.id
          return redirect("project_list")
        else:
          return HttpResponse("<h1>Your account is disabled</h1>")
      else:
        message = "Wrong username and/or password"
  else:
    form = LoginForm()
  return render(request, "login/login.html", {'form' : form, 'message' : message})

def logout_user(request):
  logout(request)
  return redirect('project_list')

def project_list(request):
  projects = get_list_or_404(Project.objects.order_by('name'))
  # Gets all critical tickets
  tickets = Ticket.objects.filter(status__status_name = "Critical")

  return render(request, 'projects/list.html', {"projects" : projects, "tickets" : tickets})

def project_add(request):
  if request.method == "POST":
    form = ProjectForm(request.POST)
    if form.is_valid():
      try:
        form.save()
        return redirect(Project.url)
      except Exception, e:
        return HttpResponseServerError()
  else:
      form = ProjectForm()
  return render(request, 'projects/add.html', {"form" : form})
  return HttpResponse('Permission denied')

def project_delete(request, project_id):
  project = get_object_or_404(Project, pk=project_id)
  project.delete();
  return redirect(Project.url)

def project_edit(request, project_id):
  project = get_object_or_404(Project, pk=project_id)
  if(request.method == "POST"):
    form = ProjectForm(request.POST, instance = project)
    if form.is_valid():
      try:
        form.save()
        return redirect(Project.url)
      except:
        return HttpResponseServerError()
  else:
    form = ProjectForm(instance = project)
  return render(request, Template_edit_project, {"form" : form, "project" : project})

def project_show(request, project_id):
  project = Project.objects.get(id=project_id)
  members = project.user
  tickets = project.tickets

  return render(request, 'projects/show.html', {"project" : project, "members" : members, "tickets" : tickets})

def project_show_tickets(request, project_id):
  project = Project.objects.get(id=project_id) 
  tickets = Project.objects.get(id=project_id).tickets.all()

  return render(request, 'projects/show_project_tickets.html', {"project" : project, "tickets" : tickets})

def ticket_show(request, project_id, ticket_id):
  project = Project.objects.get(id=project_id)
  ticket = Ticket.objects.get(id=ticket_id)

  return render(request, 'tickets/show.html', {"project" : project, "ticket" : ticket})

def project_edit_ticket(request, project_id):
  project = Project.objects.get(id=project_id)
  return render(request, 'tickets/edit.html', {"project" : project})
  
def project_delete_ticket(request, ticket_id):
  ticket = get_object_or_404(Ticket, pk=ticket_id)
  ticket.delete();
  return redirect(Ticket.url)

def projects_for_user(request):
  user = request.user
  projects = Project.objects.filter(added_by_user = user)
  return render(request, "projects/list.html", {'projects' : projects, 'headline' : 'Your projects'})