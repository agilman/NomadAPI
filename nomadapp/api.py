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
