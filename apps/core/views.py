from re import template
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ..tasks.models import Task



# Create your views here.
@login_required(login_url='/contas/login/')
def home(request):
    template_name = 'core/index.html'
    tasks = Task.objects.filter(end_date=datetime.today())

    context = {
        'tasks': tasks
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def search_tasks(request):
    template_name = 'core/search_tasks.html'
    query = request.GET.get('query')
    tasks = Task.objects.filter(name__icontains=query, owner=request.user)
    context = {
        'tasks': tasks
    }
    return render(request, template_name, context)