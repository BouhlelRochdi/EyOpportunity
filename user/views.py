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
        )
        user.save()
        return JsonResponse({'message': 'User created successfully', 'status': 201})
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

@csrf_exempt
def update(request, user_id=None):
    if request.method == 'POST':
        user = EyUser.objects.get(id=user_id)
        user.userName = request.POST.get('userName')
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.type = request.POST.get('type')
        user.save()
        return JsonResponse({'message': 'User updated successfully', 'status': 200})
    else:
        return JsonResponse({'error': 'Invalid request method', 'status': 405})


@csrf_exempt
def affectUserToEquipe(request, user_id=None):
    if request.method == 'POST':
        user = EyUser.objects.get(id=user_id)
        equipe = Equipe.objects.get(id=request.POST.get('equipe'))
        user.equipe = equipe
        user.save()
        return JsonResponse({'message': 'User updated successfully', 'status': 200})
    else:
        return JsonResponse({'error': 'Invalid request method', 'status': 405})
    

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
    try:
        user = EyUser.objects.get(id=user_id)
        email_recieved = request.POST.get('email')
        if email_recieved is not None:
            user.email = email_recieved
        userName_recieved = request.POST.get('userName')
        if userName_recieved is not None:
            user.userName = userName_recieved
        role_recieved = request.POST.get('role')
        if role_recieved is not None:
            user.role = role_recieved
        type_recieved = request.POST.get('type')
        if type_recieved is not None:
            user.type = type_recieved
        equipe_recieved = request.POST.get('equipe')
        if equipe_recieved is not None:
            user.equipe = equipe_recieved
        cv_recieved = request.FILES.get('cv')
        if cv_recieved is not None:
            user.cv = cv_recieved
        photo_recieved = request.FILES.get('photo')
        if photo_recieved is not None:
            user.photo = photo_recieved
        try:
            user.save()
            return JsonResponse({'message': 'User updated successfully', 'status': 200})
        except:
            return JsonResponse({'error': 'Error while saving user to DB', 'status': 407})
    except EyUser.DoesNotExist:
        print('User not found')
        return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
def deleteUser(request, user_id=None):
    try:
        EyUser.objects.filter(id=user_id).delete()
        return JsonResponse({'success': 'User has been deleted', 'status': 200})
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
                EyUser.objects.create(
                    userName=userName, pwd=password, email=email)
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
        userName='admin',
        pwd='admin',
        email='admin@admin',
        activated='activated',
        role='manager',
    )
    user.save()
    return JsonResponse({'message': 'admin created successfully', 'status': 200})


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
                return JsonResponse({'message': 'Invalid password or deactivated user', 'status': 301})
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

def getUserById(request, user_id=None):
    print('user_id', user_id)
    try:
        user = EyUser.objects.get(id=user_id)
        obj = {
            'id': user.id,
            'userName': user.userName,
            'email': user.email,
            'activated': user.activated,
            'role': user.role,
            'equipe': user.equipe,
        }
        return JsonResponse(obj, safe=False)
    except EyUser.DoesNotExist:
        return JsonResponse({'error': 'user not found', 'status': 404})
    
def getUserByEmail(request, email=None):
    print('email', email)
    try:
        user = EyUser.objects.get(email=email)
        obj = {
            'id': user.id,
            'userName': user.userName,
            'email': user.email,
            'activated': user.activated,
            'role': user.role,
            'equipe': user.equipe,
        }
        return JsonResponse(obj, safe=False)
    except EyUser.DoesNotExist:
        return JsonResponse({'error': 'user not found', 'status': 404})

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
def createArchive(request):
    if request.method == 'POST':
        archive = Archive(
            archiveName= request.POST.get('archiveName'),
            dueDate=request.POST.get('dueDate'),
            file=request.FILES.get('file'),
            status=request.POST.get('status'),
            progression=request.POST.get('progression'),
        )
        try:
            archive.save()
            data = {'message': 'Enregistrement réussi', 'status': 200}
            return JsonResponse(data)
        except Archive.DoesNotExist:
            return JsonResponse({'message': 'Error while creating archive', 'status': 404})
    else:
        return JsonResponse({'message': 'something went wrong', 'status': 404})


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
    try:
        archive = Archive.objects.get(id=archive_id)
        archiveName_recieved = request.POST.get('archiveName')
        if archiveName_recieved is not None:
            archive.archiveName = archiveName_recieved
        dueDate_recieved = request.POST.get('dueDate')
        if dueDate_recieved is not None:
            archive.dueDate = dueDate_recieved
        file_recieved = request.FILES.get('file')
        if file_recieved is not None:
            archive.file = file_recieved
        status_recieved = request.POST.get('status')
        if status_recieved is not None:
            archive.status = status_recieved
        progression_recieved = request.POST.get('progression')
        if progression_recieved is not None:
            archive.progression = progression_recieved
        archive.save()
        return JsonResponse({'message': 'Archive updated successfully', 'status': 200})
    except Archive.DoesNotExist:
        return JsonResponse({'error': 'Archive not found.', 'status': 404})
    
@csrf_exempt
def affectArchiveToEquipe(request, archive_id=None, equipe_id=None):
    try:
        archive = Archive.objects.get(id=archive_id)
        equipe = Equipe.objects.get(id=equipe_id)
        archive.equipe = equipe
        archive.save()
        return JsonResponse({'message': 'Archive updated successfully', 'status': 200})
    except Archive.DoesNotExist:
        return JsonResponse({'error': 'Archive not found.', 'status': 404})


def getArchiveByEquipe(request, equipe_id=None):
    try:
        archives = Archive.objects.filter(equipe=equipe_id)
        # equipe = Equipe.objects.select_related('archive_set').get(id=equipe_id)
        # archives = equipe.archive_set.all()
        for archive in archives:
            print('archive.status', archive.status)
            print('archive.progression', archive.progression)
        fullList = serializers.serialize('json', archives)
        json_data = json.loads(fullList)
        return JsonResponse(json_data, safe=False)
    
        
        
        
        # equipe = Equipe.objects.get(id=equipe_id)
        # try:
        #     archives = Archive.objects.filter(equipe_id=equipe_id)
        #     fullList = serializers.serialize('json', archives)
        #     json_data = json.loads(fullList)
        #     return JsonResponse(json_data, safe=False)
        # except Equipe.DoesNotExist:
        #     return JsonResponse({'error': 'Archive not found.', 'status': 404})
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

@csrf_exempt    
def deleteArchive(request, archive_id=None):
    try:
        Archive.objects.filter(id=archive_id).delete()
        return JsonResponse({'message': 'Archive deleted successfully', 'status': 200})
    except Archive.DoesNotExist:
        return JsonResponse({'error': 'Archive not found.', 'status': 404})
    
    
    
    
def getEquipeByArchive_old(requst, archive_id=None):
    collect_archive = []
    try:
        archives_with_equipes = Archive.objects.select_related('equipe').all()
        for archive in archives_with_equipes:
            collect_archive.append(archive)
            print('archive.status', archive.status)
            print('archive.progression', archive.progression)
        fullList = serializers.serialize('json', collect_archive)
        json_data = json.loads(fullList)
        return JsonResponse(json_data, safe=False)
    except Archive.DoesNotExist:
        return JsonResponse({'error': 'Archive not found.', 'status': 404})
    
def getUsersBelongingToEquipe(request, equipe_id=None):
    try:
        users = EyUser.objects.filter(equipe=equipe_id)
        fullList = serializers.serialize('json', users)
        json_data = json.loads(fullList)
        return JsonResponse(json_data, safe=False)
    except EyUser.DoesNotExist:
        return JsonResponse({'error': 'User not found.', 'status': 404})


def downloadArchiveFile(request, archive_id=None):
    uploaded_file = Archive.objects.get(id=archive_id)
    print('<<<<<<<<<<< uploaded_file.file.path > ', uploaded_file.file.path)
    file_path = uploaded_file.file.path
    print('<<<<<<<<<<<<<<<<< file_path > ', file_path)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=' + uploaded_file.file.name
        print('<<<<<<<<<<<<<<<<< response > ', response)
        return (response, file_path)
        return response

##################################################################################################
#################################         Equipe         ########################################

@csrf_exempt
def createEquipe(request):
    if request.method == 'POST':
        equipe = Equipe(
            equipeName=request.POST.get('equipeName'),
            project=request.POST.get('project')
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


def getMembersByEquipe(request, equipe_id=None):
    try:
        users = EyUser.objects.filter(equipe=equipe_id)
        fullList = serializers.serialize('json', users)
        json_data = json.loads(fullList)
        return JsonResponse(json_data, safe=False)
    except EyUser.DoesNotExist:
        return JsonResponse({'error': 'user not found.', 'status': 404})

# get all equipe and for each equipe five me the users belonging to it


def getAllEquipesAndUsers(request):
    fullResults = []
    try:
        equipes = Equipe.objects.all()
        obj = {}
        for equipe in equipes:
            FullObject = {}
            try:
                users = EyUser.objects.filter(equipe=equipe.id)
                FullObject['members'] = list(users.values())
            except EyUser.DoesNotExist:
                return JsonResponse({'error': 'no user found.', 'status': 404})
            FullObject['equipeName'] = equipe.equipeName
            FullObject['project'] = equipe.project
            json_data = json.dumps(FullObject)
            print('json_data', FullObject)
            obj.update({'element': json_data})
            fullResults.append(obj)
        response = HttpResponse(FullObject, content_type='application/json')

    # Set any additional headers if needed
        response['Custom-Header'] = 'Value'
        return response
        # fullList = [FullObject]  # Convert FullObject dictionary to a list of dictionaries
        # serialized_data = serializers.serialize('json', fullList)
        # json_data = json.loads(serialized_data)
        # fullResults.append(json_data)
        # return JsonResponse(fullResults, safe=False)
        # return fullList
    except Equipe.DoesNotExist:
        return JsonResponse({'error': 'Equipe not found.', 'status': 404})

        # return JsonResponse({'data': equipes}, safe=False)

        # try:
        #     user = EyUser.objects.get(equipe=equipe.id)
        #     print('user=========>', user.userName)
        # except EyUser.DoesNotExist:
        #     return JsonResponse({'error': 'user not found.', 'status': 404})

        # fullObject = {}
        # try:
        #     users = EyUser.objects.filter(equipe=equipe)
        #     fullObject['members'] = users
        #     fullObject['equipe'] = equipe
        #     fullResults.append(fullObject)
        #     print('fullResults', fullResults)
        # except EyUser.DoesNotExist:
        #     return JsonResponse({'error': 'user not found.', 'status': 404})
        # return JsonResponse({'data': equipes}, safe=False)
        
@csrf_exempt
def updateEquipe(request, equipe_id=None):
    if request.method == 'POST':
        try:
            equipe = Equipe.objects.get(id=equipe_id)
            equipeName_recieved = request.POST.get('equipeName')
            if equipeName_recieved is not None:
                equipe.equipeName = equipeName_recieved
            project_recieved = request.POST.get('project')
            if project_recieved is not None:
                equipe.project = project_recieved
            equipe.save()
            return JsonResponse({'message': 'Equipe updated successfully', 'status': 200})
        except Equipe.DoesNotExist:
            return JsonResponse({'error': 'Equipe not found.', 'status': 404})
    else:
        return JsonResponse({'message': 'Check method, it must be a POST', 'status': 403})


def getEquipeWithUsers(request):
    equipes = Equipe.objects.prefetch_related('user')
    for equipe in equipes:
        print("Equipe Name:", equipe.equipeName)
        users = equipe.eyusers.all()
    for user in users:
        print("User Name:", user.userName)
        
@csrf_exempt       
def deleteEquipe(request, equipe_id=None):
    try:
        Equipe.objects.filter(id=equipe_id).delete()
        return JsonResponse({'message': 'Equipe deleted successfully', 'status': 200})
    except Equipe.DoesNotExist:
        return JsonResponse({'error': 'Equipe not found.', 'status': 404})
