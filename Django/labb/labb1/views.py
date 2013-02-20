from django.shortcuts import get_list_or_404, render, get_object_or_404, render, redirect
from labb1.models import Project, Ticket, Status, ProjectForm, LoginForm, User, TicketForm
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError

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
          request.session["message"] = "Welcome" + user.first_name
          request.session["isLoggedIn"] = True
          request.session["user_id"] = user.id
          request.session["user"] = User.objects.get(id = user.id)
          return redirect("project_list")
        else:
          return HttpResponse("<h1>Your account is disabled</h1>")
      else:
        request.session["message"] = "Wrong username and/or password"
  else:
    form = LoginForm()
  return render(request, "login/login.html", {'form' : form})

def logout_user(request):
  logout(request)
  request.session["message"] = "You have logged out"
  request.session["isLoggedIn"] = False
  return redirect('home')

def project_list(request):
  projects = get_list_or_404(Project.objects.order_by('name'))
  user = request.user
  if request.session["isLoggedIn"]:
    # Gets all critical tickets
    tickets = Ticket.objects.filter(status__status_name = "Critical")
    return render(request, 'projects/list.html', {"projects" : projects, "tickets" : tickets, "user" : user})
  else:
    request.session["message"] = "You need to be logged in to view this."
    return redirect("login")

def project_add(request):
  if request.method == "POST":
    form = ProjectForm(request.POST)
    if form.is_valid():
      form.instance.date_added = datetime.date.today()
      form.instance.date_updated = datetime.date.today()
      form.instance.owner = request.user
      try:
        form.save()
        request.session["message"] = "Successfully added your project"
        return redirect("project_list")
      except:
        return HttpResponseServerError()
  else:
      form = ProjectForm()
  return render(request, 'projects/add.html', {"form" : form})
  return HttpResponse('Permission denied')

def project_delete(request, project_id):
  user = request.user
  project = get_object_or_404(Project, pk=project_id)
  if project.owned_by_user(request.user): 
    project.delete()
    request.session["message"] = "The project has been removed"
    return redirect ('project_list')
  else:
    request.session["message"] = "You have no permission to delete this project"
    return render(request, 'projects/show.html', {"project" : project})

def project_edit(request, project_id):
  project = get_object_or_404(Project, pk=project_id)
  if project.owned_by_user(request.user):
    if(request.method == "POST"):
      form = ProjectForm(request.POST, instance = project)
      if form.is_valid():
        try:
          form.save()
          return redirect('project_list')
        except:
          return HttpResponseServerError()
    else:
      form = ProjectForm(instance = project)
    return render(request, 'projects/edit.html', {"form" : form, "project" : project})
  else:
    request.session["message"] = "You are not allowed to edit this project."
    return render(request, 'projects/show.html', {"project" : project})

def project_show(request, project_id):
  if request.session["isLoggedIn"]:
    project = Project.objects.get(id=project_id)
    members = project.user
    tickets = project.tickets   
    return render(request, 'projects/show.html', {"project" : project, "members" : members, "tickets" : tickets})
  else:
    request.session["message"] = "You need to be logged in to view this."
    return redirect("login")

def project_show_tickets(request, project_id):
  if request.session["isLoggedIn"]:
    project = Project.objects.get(id=project_id) 
    tickets = Project.objects.get(id=project_id).tickets.all()
    return render(request, 'projects/show_project_tickets.html', {"project" : project, "tickets" : tickets})
  else:
    request.session["message"] = "You need to be logged in to view this."
    return redirect("login")

def project_join(request, project_id):
  project = Project.objects.get(id = project_id)
  user = request.user
  if not project.member_in_project(user):
    project.user = user
    project.save
    return render(request, "projects/show.html", {"project" : project})

def ticket_show(request, project_id, ticket_id):
  if request.session["isLoggedIn"]:
    project = Project.objects.get(id=project_id)
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'tickets/show.html', {"project" : project, "ticket" : ticket})
  else:
    request.session["message"] = "You need to be logged in to view this."
    return redirect("login")

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
          return render(request, 'tickets/show.html', {"project" : project, "ticket" : ticket})
        except:
          return HttpResponseServerError()
    else:
      form = TicketForm(instance = ticket)
    return render(request, 'tickets/edit.html', {"form" : form, "ticket" : ticket, "project" : project})
  else:
    request.session["message"] = "You have no permission to edit this ticket"
    return render(request, 'tickets/show.html', {"project" : project, "ticket" : ticket})
  
def project_delete_ticket(request, project_id, ticket_id):
  project = get_object_or_404(Project, pk = project_id)
  ticket = get_object_or_404(Ticket, pk=ticket_id)
  if project.owned_by_user(request.user) or ticket.owned_by_user(request.user):
    ticket.delete();
    return render(request, "projects/show.html", {"project" : project})
  else:
    request.session["message"] = "You have no permission to delete this ticket"
    return render(request, 'projects/show.html', {"project" : project})

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
          request.session["message"] = "Successfully added a ticket"
          tickets = project.tickets
          return render(request, "projects/show.html", {"project" : project, "tickets" : tickets})
        except:
          return HttpResponseServerError()
    else:
        form = TicketForm()
    return render(request, 'tickets/add.html', {"form" : form, "project" : project})
    return HttpResponse('Permission denied')
  else:
    request.session["message"] = "You have no permission to add a ticket, you need to be a member of the project."
    return render(request, 'projects/show.html', {"project" : project})

def home(request):

  return render(request, "home/index.html")