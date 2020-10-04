from nomadapp.models import *
from nomadapp.serializers import *

from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def user(request,userName=None):
    if request.method == 'GET':
        try:
          user = User.objects.get(username=userName)
          serialized = UserSerializer(user).data
        except User.DoesNotExist:
            serialized = []
            

        return JsonResponse(serialized, safe=False)

    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['allow'] = ','.join(['get','options'])
        return response

@csrf_exempt
def adventures(request,advId=None):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        userId = int(data["user"])
        print("Hello", userId)
        #TODO: VALIDATION
        user = User.objects.get(pk=userId)

        advName = data["advName"]
        advType = data["advType"]
        advStatus = data["advStatus"]

        #TODO
        #If advStatus = active, need to unset previous active.

        adv = Adventure(name=advName,user=user,advType=advType,advStatus=advStatus)
        adv.save()

        #create directory
        #media_root = settings.USER_MEDIA_ROOT
        #os.mkdir(media_root + "/" + str(userId)+"/"+str(adv.id))
        #os.mkdir(media_root + "/" + str(userId)+"/"+str(adv.id)+"/gear")

        serialized = AdventureSerializer(adv)
        return JsonResponse(serialized.data,safe=False)

    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['allow'] = ','.join(['get','options'])
        return response
