from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, CommentForm, ProjectForm
from django.contrib.auth.decorators import login_required
from .models import Task, Project, Tag
from django.http import Http404

def is_htmx(request):
    return request.headers.get('HX-Request') == 'true'

def home(request):
    return render(request, 'tasks/home.html')

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()
            tasks = Task.objects.filter(user=request.user)
            if is_htmx(request):
                return render(request, 'tasks/partials/task_list.html', {'tasks': tasks})
            return redirect('tasks:task_list')
    else:
        form = TaskForm()
    template = 'tasks/partials/create_task_form.html' if is_htmx(request) else 'tasks/create_task.html'
    return render(request, template, {'form': form})


@login_required
def edit_task(request, pk):
    task = request.user.tasks.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            tasks = Task.objects.filter(user=request.user)
            if is_htmx(request):
                return render(request, 'tasks/partials/task_list.html', {'tasks': tasks})
            return redirect('tasks:task_list')
    else:
        form = TaskForm(instance=task)
    template = 'tasks/partials/edit_task_form.html' if is_htmx(request) else 'tasks/edit_task.html'
    return render(request, template, {'form': form, 'task': task})


@login_required
def delete_task(request, pk):
    task = request.user.tasks.get(pk=pk)
    if request.method == 'POST':
        task.delete()
        tasks = Task.objects.filter(user=request.user)
        if is_htmx(request):
            return render(request, 'tasks/partials/task_list.html', {'tasks': tasks})
        return redirect('tasks:task_list')
    template = 'tasks/partials/delete_task_confirm.html' if is_htmx(request) else 'tasks/delete_task.html'
    return render(request, template, {'task': task})


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    template = 'tasks/partials/task_list.html' if is_htmx(request) else 'tasks/task_list.html'
    return render(request, template, {'tasks': tasks})

@login_required
def add_comment(request, task_id):
    from .forms import CommentForm
    from .models import Task
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return redirect('tasks:task_detail', task_id=task.id)
    else:
        form = CommentForm()
    return render(request, 'tasks/add_comment.html', {'form': form, 'task': task})

@login_required
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.user != request.user:
        raise Http404("You do not have permission to view this task.")
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            projects = request.user.projects.all()
            if is_htmx(request):
                return render(request, 'tasks/partials/project_list.html', {'projects': projects})
            return redirect('tasks:project_list')
    else:
        form = ProjectForm()
    template = 'tasks/partials/create_project_form.html' if is_htmx(request) else 'tasks/create_project.html'
    return render(request, template, {'form': form})


@login_required
def edit_project(request, pk):
    project = request.user.projects.get(pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            projects = request.user.projects.all()
            if is_htmx(request):
                return render(request, 'tasks/partials/project_list.html', {'projects': projects})
            return redirect('tasks:project_list')
    else:
        form = ProjectForm(instance=project)
    template = 'tasks/partials/edit_project_form.html' if is_htmx(request) else 'tasks/edit_project.html'
    return render(request, template, {'form': form, 'project': project})


@login_required
def delete_project(request, pk):
    project = request.user.projects.get(pk=pk)
    if request.method == 'POST':
        project.delete()
        projects = request.user.projects.all()
        if is_htmx(request):
            return render(request, 'tasks/partials/project_list.html', {'projects': projects})
        return redirect('tasks:project_list')
    template = 'tasks/partials/delete_project_confirm.html' if is_htmx(request) else 'tasks/delete_project.html'
    return render(request, template, {'project': project})


@login_required
def project_list(request):
    projects = request.user.projects.all()
    template = 'tasks/partials/project_list.html' if is_htmx(request) else 'tasks/project_list.html'
    return render(request, template, {'projects': projects})


@login_required
def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'tasks/project_detail.html', {'project': project})


@login_required
def task_tags_add(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        tag_name = request.POST.get('tag_name')
        if tag_name:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            task.tags.add(tag)
            return redirect('tasks:task_detail', task_id=task.id)
    return render(request, 'tasks/add_tag.html', {'task': task})

@login_required
def tasks_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tasks = tag.tasks.filter(user=request.user)
    return render(request, 'tasks/tasks_by_tag.html', {'tag': tag, 'tasks': tasks})

