from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
import os

from rest_framework.parsers import JSONParser

from nomadapp.serializers import *
# Create your views here.

@csrf_exempt
def registration(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        # TODO: Validate data!!!
        nu = {
            'username' : data['username'],
            'email' : data['email'],
            'password' :data['password']
        }

        # TODO handle errors...
        newUser = User.objects.create_user(nu['username'],nu['email'],nu['password'])
        newUser.save()

        #create directory for user media
        target = os.path.join(settings.USER_MEDIA_ROOT, str(newUser.id))
        target2 = os.path.join(target ,'profile_pictures')
        os.mkdir(target)
        os.mkdir(target2)
        return JsonResponse(UserSerializer(newUser).data,safe=False)

    elif request.method == 'OPTIONS':
        response = HttpResponse()
        response['allow'] = ','.join(['POST','OPTIONS'])
        return response

@csrf_exempt
def logout_view(request):
    logout(request)

    return redirect('/')
