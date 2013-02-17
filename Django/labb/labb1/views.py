from django.shortcuts import get_list_or_404, render
from labb1.models import Project, Ticket, Status, ProjectForm

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