from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import User


def index(request):
    users = User.objects.all()

    context = { 'users': users }

    if 'edit_id' in request.GET:
        context = { **context, 'message': 'edit', 'message_id': request.GET['edit_id'] }
    
    if 'delete_id' in request.GET:
        context = { **context, 'message': 'delete', 'message_id': request.GET['delete_id'] }

    template = loader.get_template('user/index.html')
    return HttpResponse(template.render(context, request))


def create_new(request):

    if request.method == 'POST':
        user = User(            
            userName=request.POST['userName'],
            email=request.POST['email'],
            role=request.POST['role'],
            type=request.POST['type'],
            equipe=request.POST['equipe']
        )
        user.save()
        return HttpResponseRedirect(reverse('users_index') + '?edit_id=' + str(user.id))

    context = {}
    template = loader.get_template('user/create.html')
    return HttpResponse(template.render(context, request))


def view(request, user_id=None):
    user = User.objects.filter(id=user_id).first()
    context = { 'user': user }
    template = loader.get_template('user/view.html')
    return HttpResponse(template.render(context, request))


def edit(request, user_id=None):
    user = User.objects.filter(id=user_id).first()

    if request.method == 'POST':
        user.userName=request.POST['userName']
        user.email=request.POST['email']
        user.role=request.POST['role']
        user.type=request.POST['type']
        user.equipe=request.POST['equipe']
        
        
        user.save()
        return HttpResponseRedirect(reverse('users_index') + '?edit_id=' + str(user.id))

    context = { 'user': user }
    template = loader.get_template('user/edit.html')
    return HttpResponse(template.render(context, request))


def delete(request, user_id=None):
    user = User.objects.filter(id=user_id).first()

    if request.method == 'POST':
        user = User.objects.filter(id=user_id).delete()
        return HttpResponseRedirect(reverse('users_index') + '?delete_id=' + str(user_id))

    context = { 'user': user }
    template = loader.get_template('user/delete.html')
    return HttpResponse(template.render(context, request))