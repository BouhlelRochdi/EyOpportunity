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
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


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
    if request.method == 'POST':
        user = EyUser(
            userName=request.POST.get('userName'),
            email=request.POST.get('email'),
            role=request.POST.get('role'),
            type=request.POST.get('type'),
            equipe=request.POST.get('equipe')
        )
        user.save()
        fullList = serializers.serialize('json', user)
        json_data = json.loads(fullList)
        return JsonResponse(json_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method', 'status': 405})


def view(request, user_id=None):
    user = EyUser.objects.filter(id=user_id).first()
    context = {'user': user}
    template = loader.get_template('user/view.html')
    return HttpResponse(template.render(context, request))

def decodeToken(access_token):
    if access_token:
        # Extract the access token
        try:
            token = access_token.split(' ')[1]
            decoded_token = AccessToken(token)
            payload = decoded_token.payload
            return payload
        except (IndexError, InvalidToken):
            # Handle invalid token or missing token in header
            return JsonResponse({'error': 'Invalid or missing access token', 'status': 401})
    # If the authorization header is not found
    return JsonResponse({'error': 'Authorization header not found', 'status': 401})

def checkTokenPayload(payload):
    if payload:
        try:
            user = EyUser.objects.get(id=payload['user_id'])
            return user
        except EyUser.DoesNotExist:
            return JsonResponse({'error': 'User not found', 'status': 404})
    else:
        return JsonResponse({'error': 'no token exist', 'status': 401})


@csrf_exempt
def edit(request, user_id=None):
    authorization_header = request.headers.get('Authorization')
    payload = decodeToken(authorization_header)
    if payload:
        try:
            user = EyUser.objects.get(id=user_id)
            if user.id == payload['user_id']:
                data = request.POST  # Assumes form data is sent in the request body
                model_fields = [
                    field.name for field in EyUser._meta.get_fields()]
                for field, value in data.items():
                    if field in model_fields:
                        setattr(user, field, value)
                user.save()
                fullList = serializers.serialize('json', user)
                json_data = json.loads(fullList)
                # Utiliser JsonResponse pour renvoyer la réponse JSON
                return JsonResponse(json_data, safe=False)
            else:
                return JsonResponse({'error': 'you do not have the permission to edit this user'}, status=401)
        except EyUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'no token exist', 'status': 401})


def delete(request, user_id=None):
    authorization_header = request.headers.get('Authorization')
    payload = decodeToken(authorization_header)
    user = checkTokenPayload(payload)
    try:
        user = checkTokenPayload(payload)
        if user.id == user_id:
            if request.method == 'POST':
                user = EyUser.objects.filter(id=user_id).delete()
                return JsonResponse({'success': 'User has been deleted', 'status': 200})
        else:
            return JsonResponse({'error': 'you do not have the permission to edit this user', 'status': 401})
    except EyUser.DoesNotExist:
        return JsonResponse({'error': 'User not found', 'status': 404})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        userName_arrived = request.POST.get('userName'),
        email_arrived = request.POST.get('email'),
        password = request.POST.get('password')
        email = str(email_arrived[0]).strip("(),'")
        userName = str(userName_arrived[0]).strip("(),'")
        userFounded = EyUser.objects.filter(email=email).exists()
        if userFounded:
            data = {'message': 'L\'utilisateur existe deja', 'status': 403}
            return JsonResponse(data)
        else:
            try:
                EyUser.objects.create(userName=userName, pwd=password, email=email)
                return JsonResponse({'message': 'L\'utilisateur a ete creer avec success', 'status': 200})
            except EyUser.DoesNotExist:
                return JsonResponse({'error': 'Something went wrong', 'status': 403})
    return JsonResponse({'message': 'Méthode non autorisée', 'status': 'error'})
    

def getAllUsers(request):
    try:
        users = EyUser.objects.all()
        fullList = serializers.serialize('json', users)
        json_data = json.loads(fullList)
        return JsonResponse(json_data, safe=False)
    except EyUser.DoesNotExist:
        return JsonResponse({'error': 'no users found', 'status': 404})

@csrf_exempt
def activateUser(request, id=None):
    role_arrived = request.POST.get('role')
    role = str(role_arrived).strip("(),'")
    try:
        userToActivate = EyUser.objects.get(id=id)
        userToActivate.activated = 'activated'
        userToActivate.role = role
        userToActivate.save()
        return HttpResponse({'success': 'user has been activated successfully', 'status': 200})
    except EyUser.DoesNotExist:
        return JsonResponse({'error': 'user not found', 'status': 404})
    
def createAdmin(request):
    user = EyUser(
        userName= 'admin',
        pwd= 'admin',
        email= 'admin@admin',
        activated= 'activated',
        role= 'manager',
    )
    user.save()
    return JsonResponse({'message': 'admin created successfully', 'status': 200})
        
    
    
    
    # if user_connected is None:
    #     return JsonResponse({'error': 'you need to connect before', 'status': 401})
    # else:
    #     try:
    #         userToActivate = EyUser.objects.get(id=id)
            
    # elif user.activated == 'activated':
    #     return JsonResponse({'error': 'user already activated', 'status': 301})
    # else:
    #     user.activated = 'activated'
    #     user.save()
    #     return JsonResponse({'success': 'user has been activated successfully', 'status': 200})


@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print('email', email)
        print('password', password)
        try:
            user = EyUser.objects.get(email=email)
            print('user', user)
            print('user.pwd', user.pwd)
            if user.pwd == password:
                token = AccessToken.for_user(user)
                user.access_token = token
                user.save()
                userFounded = EyUser.objects.filter(email=email)
                fullList = serializers.serialize('json', userFounded)
                json_data = json.loads(fullList)
                return JsonResponse(json_data, safe=False)
            else:
                return JsonResponse({'message': 'Invalid password', 'status': 301})
        except EyUser.DoesNotExist:
            return JsonResponse({'message': 'Invalid email', 'status': 301})
    else:
        return JsonResponse({'message': 'request must be a POST', 'status': 402})

def sign_out(request):
    authorization_header = request.headers.get('Authorization')
    payload = decodeToken(authorization_header)
    user = checkTokenPayload(payload)
    if user is None:
        return JsonResponse({'error': 'user not found', 'status': 404})
    else:
        user.access_token = None
        user.save()
        return JsonResponse({'success': 'user has been logged out successfully', 'status': 200})

def getConnectedUser(request):
    authorization_header = request.headers.get('Authorization')
    payload = decodeToken(authorization_header)
    user = checkTokenPayload(payload)
    if user is None:
        return JsonResponse({'error': 'user not found', 'status': 404})
    else:
        fullList = serializers.serialize('json', user)
        json_data = json.loads(fullList)
        return JsonResponse(json_data, safe=False)
    
def getDeactivatedUsers(request):
    try:
        users = EyUser.objects.filter(activated='deactivated')
        fullList = serializers.serialize('json', users)
        json_data = json.loads(fullList)
        return JsonResponse(json_data, safe=False)
    except EyUser.DoesNotExist:
        return JsonResponse({'error': 'no users found', 'status': 404})
    
def getActivatedUsers(request):
    try:
        users = EyUser.objects.filter(activated='activated')
        fullList = serializers.serialize('json', users)
        json_data = json.loads(fullList)
        return JsonResponse(json_data, safe=False)
    except EyUser.DoesNotExist:
        return JsonResponse({'error': 'no users found', 'status': 404})

##################################################################################################
#################################         Archive         ########################################

@csrf_exempt
def createArchive(request, user_id=None, equipe_id=None):
    authorization_header = request.headers.get('Authorization')
    payload = decodeToken(authorization_header)
    user = checkTokenPayload(payload)
    if user.id == user_id:
        if request.method == 'POST':
            archive = Archive(
                archiveName=request.POST.get('archiveName'),
                archiveData=request.FILES.get('file')
            )
            try:
                equipe = Equipe.objects.get(id=equipe_id)
                archive.user = user
                archive.equipe = equipe
                archive.save()
                data = {'message': 'Enregistrement réussi', 'status': 200}
                return JsonResponse(data)
            except EyUser.DoesNotExist:
                return JsonResponse({'message': 'user who want to add archive is not found', 'status': 401})
        else:
            return JsonResponse({'message': 'something went wrong', 'status': 404})
    return JsonResponse({'message': 'user invalid', 'status': 401})


def getFullArchive(request):
    archives = Archive.objects.all()
    if archives is None:
        data = {'message': 'no archive found', 'status': 404}
        return JsonResponse(data)
    else:
        fullList = serializers.serialize('json', archives)
        json_data = json.loads(fullList)
    # Utiliser JsonResponse pour renvoyer la réponse JSON
    return JsonResponse(json_data, safe=False)


def getArchiveByUser(request, user_id=None):
    authorization_header = request.headers.get('Authorization')
    payload = decodeToken(authorization_header)
    user = checkTokenPayload(payload)
    if user.id != user_id:
        return JsonResponse({'message': 'user invalid', 'status': 401})
    else:
        try:
            archives = Archive.objects.filter(user=user)
            fullList = serializers.serialize('json', archives)
            json_data = json.loads(fullList)
            return JsonResponse(json_data, safe=False)
        except Archive.DoesNotExist:
            return JsonResponse({'message': 'Archive does not exist', 'status': 401})

@csrf_exempt
def update_archive(request, archive_id=None):
    authorization_header = request.headers.get('Authorization')
    payload = decodeToken(authorization_header)
    user = checkTokenPayload(payload)
    if user is None:
        return JsonResponse({'error': 'you are not Authenticated.', 'status': 401})
    else:
        archive = Archive(
            archiveName=request.POST.get('archiveName'),
            archiveData=request.FILES.get('file'),
            status=request.POST.get('status'),
            progression=request.POST.get('progression')
        )
        try:
            archive = Archive.objects.get(id=archive_id)
            archive.save()
        except Archive.DoesNotExist:
            return JsonResponse({'error': 'Archive not found.', 'status': 404})
        
def getArchiveByEquipe(request, equipe_id=None):
    try:
        equipe = Equipe.objects.get(id=equipe_id)
        try:
            archives = Archive.objects.filter(equipe_id=equipe_id)
            fullList = serializers.serialize('json', archives)
            json_data = json.loads(fullList)
            return JsonResponse(json_data, safe=False)
        except Equipe.DoesNotExist:
            return JsonResponse({'error': 'Archive not found.', 'status': 404})
    except Equipe.DoesNotExist:
            return JsonResponse({'error': 'Equipe not found.', 'status': 404})
        
def getArchiveByStatus(request, status=None):
    try:
        archives = Archive.objects.filter(status=status)
        fullList = serializers.serialize('json', archives)
        json_data = json.loads(fullList)
        return JsonResponse(json_data, safe=False)
    except Archive.DoesNotExist:
        return JsonResponse({'error': 'Archive not found.', 'status': 404})

def getArchiveByProgression(request, progression=None):
    try:
        archives = Archive.objects.filter(progression=progression)
        fullList = serializers.serialize('json', archives)
        json_data = json.loads(fullList)
        return JsonResponse(json_data, safe=False)
    except Archive.DoesNotExist:
        return JsonResponse({'error': 'Archive not found.', 'status': 404})
    


##################################################################################################
#################################         Equipe         ########################################

@csrf_exempt
def createEquipe(request):

    if request.method == 'POST':
        equipe = Equipe(
            equipeName=request.POST.get('equipeName'),
            equipeDesc=request.POST.get('equipeDesc')
        )
        try:
            equipe.save()
            return JsonResponse({'message': 'Enregistrement réussi', 'status': 'success', 'status': 200})
        except Archive.DoesNotExist:
            return JsonResponse({'error': 'Model does not exist.', 'status': 404})
    else:
        return JsonResponse({'message': 'Check method, it must be a POST', 'status': 403})


def getAllEquipes(request):
    equipes = Equipe.objects.all()
    if equipes is None:
        data = {'message': 'no equipe found', 'status': 'error'}
        return JsonResponse(data)
    else:
        fullList = serializers.serialize('json', equipes)
        json_data = json.loads(fullList)
    # Utiliser JsonResponse pour renvoyer la réponse JSON
    return JsonResponse(json_data, safe=False)

# get equipe and users belonging to it
def getEquipeById(request, equipe_id=None):
    try:
        equipe = Equipe.objects.get(id=equipe_id)
        try:
            users = EyUser.objects.filter(equipe=equipe)
            fullList = serializers.serialize('json', users)
            json_data = json.loads(fullList)
            return JsonResponse(json_data, safe=False)
        except EyUser.DoesNotExist:
            return JsonResponse({'error': 'user not found.', 'status': 404})
    except Equipe.DoesNotExist:
        return JsonResponse({'error': 'Equipe not found.', 'status': 404})
    
# get all equipe and for each equipe five me the users belonging to it
def getAllEquipesAndUsers(request):
    equipes = Equipe.objects.all()
    if equipes is None:
        data = {'message': 'no equipe found', 'status': 'error'}
        return JsonResponse(data)
    else:
        fullList = serializers.serialize('json', equipes)
        json_data = json.loads(fullList)
        for equipe in equipes:
            try:
                users = EyUser.objects.filter(equipe=equipe)
                fullList = serializers.serialize('json', users)
                json_data = json.loads(fullList)
                return JsonResponse(json_data, safe=False)
            except EyUser.DoesNotExist:
                return JsonResponse({'error': 'user not found.', 'status': 404})
    # Utiliser JsonResponse pour renvoyer la réponse JSON
    return JsonResponse(json_data, safe=False)