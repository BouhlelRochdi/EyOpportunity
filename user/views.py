import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import EyUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


def index(request):
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
    print('---------------- we are in --------------------')
    if request.method == 'POST':
        user = EyUser(
            userName=request.POST.get('userName', False),
            email=request.POST.get('email', False),
            role=request.POST.get('role', False),
            type=request.POST.get('type', False),
            equipe=request.POST.get('equipe', False)
        )
        user.save()
        return HttpResponseRedirect(reverse('users_index') + '?edit_id=' + str(user.id))

    context = {}
    template = loader.get_template('user/create.html')
    return HttpResponse(template.render(context, request))


def view(request, user_id=None):
    user = EyUser.objects.filter(id=user_id).first()
    context = {'user': user}
    template = loader.get_template('user/view.html')
    return HttpResponse(template.render(context, request))


def edit(request, user_id=None):
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
    user = EyUser.objects.filter(id=user_id).first()

    if request.method == 'POST':
        user = EyUser.objects.filter(id=user_id).delete()
        return HttpResponseRedirect(reverse('users_index') + '?delete_id=' + str(user_id))

    context = {'user': user}
    template = loader.get_template('user/delete.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def register(request):
    if request.method == 'POST':
        userName = request.POST.get('userName', False),
        email = request.POST.get('email', False),
        password = request.POST.get('password', False)

        if EyUser.objects.filter(email=email).exists():
            # L'utilisateur existe déjà
            data = {'message': 'L\'utilisateur existe déjà', 'status': 'error'}
        else:
            # Création d'un nouvel utilisateur
            user = EyUser.objects.create(
                userName=userName, password=password, email=email)
            # Vous pouvez également ajouter d'autres champs personnalisés à l'utilisateur ici

            # Envoi d'une réponse JSON
            data = {'message': 'Enregistrement réussi', 'status': 'success'}

        return JsonResponse(data, status=200)

    # Si la méthode de requête n'est pas POST, renvoyer une réponse d'erreur
    return JsonResponse({'message': 'Méthode non autorisée', 'status': 'error'})


def getAllUsers(request):
    users = EyUser.objects.all()
    if users is None:
        data = {'message': 'no users found', 'status': 'error'}
        return JsonResponse(data)
    else:
        fullList = serializers.serialize('json', users)
        json_data = json.loads(fullList)
    # Utiliser JsonResponse pour renvoyer la réponse JSON
    return JsonResponse(json_data, safe=False)


def activateUser(request, user_id=None):
    user = EyUser.objects.filter(id=user_id).first()
    # context = {'user': user}
    if user is None:
        data = {'message': 'no users found', 'status': 'error'}
    elif user.activated == 'allow':
        data = {'message': 'user already activated', 'status': 'error'}
    else:
        user.activateUser = 'allow'

    t#emplate = loader.get_template('user/view.html')
    return JsonResponse(user, safe=False)







