import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import EyUser, Archive, Equipe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib import messages
import random
import string
from django.core.serializers import serialize
from django.db.models.query import QuerySet


def index(request):
    print('---------------- we are in index --------------------')
    users = EyUser.objects.all()

    context = {'users': users}

    if 'edit_id' in request.GET:
        context = {**context, 'message': 'edit',
                   'message_id': request.GET['edit_id']}

    if 'delete_id' in request.GET:
        context = {**context, 'message': 'delete',
                   'message_id': request.GET['delete_id']}

    template = loader.get_template('user/index.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def create_new(request):
    print('---------------- we are in create new --------------------')
    if request.method == 'POST':
        user = EyUser(
            userName=request.POST.get('userName'),
            email=request.POST.get('email'),
            role=request.POST.get('role'),
            type=request.POST.get('type'),
            equipe=request.POST.get('equipe')
        )
        user.save()
        return HttpResponseRedirect(reverse('users_index') + '?edit_id=' + str(user.id))

    context = {}
    template = loader.get_template('user/create.html')
    return HttpResponse(template.render(context, request))


def view(request, user_id=None):
    print('---------------- we are in view --------------------')
    user = EyUser.objects.filter(id=user_id).first()
    context = {'user': user}
    template = loader.get_template('user/view.html')
    return HttpResponse(template.render(context, request))


def edit(request, user_id=None):
    print('---------------- we are in edit --------------------')
    user = EyUser.objects.filter(id=user_id).first()

    if request.method == 'POST':
        user.userName = request.POST['userName']
        user.email = request.POST['email']
        user.role = request.POST['role']
        user.type = request.POST['type']
        user.equipe = request.POST['equipe']
        user.save()
        return HttpResponseRedirect(reverse('users_index') + '?edit_id=' + str(user.id))

    context = {'user': user}
    template = loader.get_template('user/edit.html')
    return HttpResponse(template.render(context, request))


def delete(request, user_id=None):
    print('---------------- we are in delete --------------------')
    user = EyUser.objects.filter(id=user_id).first()

    if request.method == 'POST':
        user = EyUser.objects.filter(id=user_id).delete()
        return HttpResponseRedirect(reverse('users_index') + '?delete_id=' + str(user_id))

    context = {'user': user}
    template = loader.get_template('user/delete.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def register(request):
    print('---------------- we are in register --------------------')
    if request.method == 'POST':
        userName_arrived = request.POST['userName'],
        email_arrived = request.POST['email'],
        password = request.POST['password']
        email = str(email_arrived[0]).strip("(),'")
        userName = str(userName_arrived[0]).strip("(),'")

        if EyUser.objects.filter(email=email).exists():
            # L'utilisateur existe déjà
            data = {'message': 'L\'utilisateur existe déjà', 'status': 'error'}
        else:
            # Création d'un nouvel utilisateur
            EyUser.objects.create(userName=userName, pwd=password, email=email)
            # Vous pouvez également ajouter d'autres champs personnalisés à l'utilisateur ici

            # Envoi d'une réponse JSON
            data = {'message': 'Enregistrement réussi', 'status': 'success'}

        return JsonResponse(data, status=200)

    # Si la méthode de requête n'est pas POST, renvoyer une réponse d'erreur
    return JsonResponse({'message': 'Méthode non autorisée', 'status': 'error'})


def getAllUsers(request):
    users = EyUser.objects.all()
    for ey_user in users:
        print('user name => ', ey_user.userName)
        # print('email => ', ey_user.email)
        # print("role => ", ey_user.role)
        # print('id => ', ey_user.id)
    if users is None:
        data = {'message': 'no users found', 'status': 'error'}
        return JsonResponse(data)
    else:
        fullList = serializers.serialize('json', users)
        json_data = json.loads(fullList)
    # Utiliser JsonResponse pour renvoyer la réponse JSON
    return JsonResponse(json_data, safe=False)


def activateUser(request, id=None):
    user = EyUser.objects.filter(id=id).first()
    if user is None:
        data = {'message': 'no users found', 'status': 'error'}
    elif user.activated == 'activated':
        data = {'message': 'user already activated', 'status': 'error'}
    else:
        user.activated = 'activated'
        user.save()
        return HttpResponseRedirect(reverse('users_index') + '?id=' + str(id))
    # emplate = loader.get_template('user/view.html')
    userToReturn = serializers.serialize('json', user)
    return JsonResponse(userToReturn, safe=False)


@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print('email==== ', email)
        print('password==== ', password)
        try:
            user = EyUser.objects.get(email=email)
            if user.pwd == password:
                # Log in the user
                token = ''.join(random.choices(
                    string.ascii_letters + string.digits, k=16))
                user.access_token = token
                user.save()
                data = {'message': 'login success', 'status': 'success'}
                print('user success login')
                return JsonResponse(user, data, safe=False)
            else:
                return JsonResponse({'message': 'Invalid password', 'status': 'error'})
        except EyUser.DoesNotExist:
            return JsonResponse({'message': 'Invalid email', 'status': 'error'})
    else:
        return JsonResponse({'message': 'request must be a POST', 'status': 'error'})


##################################################################################################
#################################         Archive         ########################################

@csrf_exempt
def createArchive(request, user_id=None):
    if request.method == 'POST':
        archive = Archive(
            archiveName=request.POST.get('archiveName'),
            archiveData=request.FILES.get('file')
        )
        try:
            user = EyUser.objects.get(id=user_id)
            archive.user = user
            archive.save()
            data = {'message': 'Enregistrement réussi', 'status': 'success'}
            return JsonResponse(data, status=200)
        except EyUser.DoesNotExist:
            return JsonResponse({'message': 'user not found', 'status': 401})
    else:        
        return JsonResponse({'message': 'something went wrong', 'status': 'error'})


def getFullArchive(request):
    archives = Archive.objects.all()
    for archive in archives:
        print('user name => ', archive.archiveName)
        # print('email => ', ey_user.email)
        # print("role => ", ey_user.role)
        # print('id => ', ey_user.id)
    if archive is None:
        data = {'message': 'no archive found', 'status': 'error'}
        return JsonResponse(data)
    else:
        fullList = serializers.serialize('json', archives)
        json_data = json.loads(fullList)
    # Utiliser JsonResponse pour renvoyer la réponse JSON
    return JsonResponse(json_data, safe=False)
