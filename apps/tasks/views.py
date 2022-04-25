from email import message
from re import template
from unicodedata import category
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CategoryForm, TaskForm
from django.contrib import messages
from .models import Category, Task
from django.contrib.auth.decorators import login_required


import time
from django.db import connection
import datetime
from datetime import timedelta


# Create your views here.
@login_required(login_url='/contas/login/')
def add_category(request):
    template_name = 'tasks/add_category.html'
    context = {}
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj = form.save()
            obj.save()
            messages.success(request, 'Categoria adicionado com sucesso')
    form = CategoryForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_categories(request):
    tempo_inicial = time.time()
    template_name = 'tasks/list_categories.html'
    categories = Category.objects.filter(owner=request.user)
    tempo_final = time.time()
    query = connection.queries
    queries = len(query)


    now = datetime.datetime.now()
    dias = now + timedelta(days=3)



    tempo_execucao =  tempo_final - tempo_inicial
    context = {
        'categories': categories,
        'tempo_execucao': tempo_execucao,
        'queries': queries,
        'dias': dias,


        
    }
    tempo_final = time.time()
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_category(request, id=None):
    template_name = 'tasks/add_category.html'
    context = {}
    category = get_object_or_404(Category, id=id, owner=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('tasks:list_categories')
    form = CategoryForm(instance=category)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_category(request, id):
    category = Category.objects.get(id=id)
    if category.owner == request.user:
        category.delete()
    else:
        message.error(request, 'Você não pode excluir')
        return redirect('core:home')
    return redirect('tasks:list_categories')

# =================== TASKS ========================================
@login_required(login_url='/contas/login/')
def add_task(request):
    template_name = 'tasks/add_task.html'
    context = {}
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            form.save_m2m
            messages.success(request, 'Tarefa adicionada com sucesso')
        else:
            print(form.error)
    form = TaskForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def tasks_list(request):
    template_name = 'tasks/tasks_list.html'
    context = {}
    tasks = Task.objects.filter(owner=request.user)
    context['tasks'] = tasks
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_task(request, id_task):
    template_name = 'tasks/add_task.html'
    context = {}
    task = get_object_or_404(Task, id=id_task, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:tasks_list')
    form = TaskForm(instance=task)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def task_delete(request, id_task):
    task =Task.objects.get(id=id_task)
    if task.owner == request.user:
        task.delete()
  
    else:
        message.error(request, 'Você não pode excluir')
        return redirect('core:home')
    return redirect('tasks:tasks_list') 
