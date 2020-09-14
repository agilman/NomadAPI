from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from nomadapp.serializers import *
from nomadapp import forms
# Create your views here.

@csrf_exempt
def registration(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)

        print(dir(form))
        print(form.data)
        print("YES< THIS IS A POST REQUEST RECEIVED")
        if form.is_valid():
            newUser = form.save()
            serialized = UserSerializer(user).data
            #return newUser serialized
            print("New user registered successfully")
            print(serialized)
            return JsonResponse(serialized, safe=False)
                #assign session
            #login(request,newUser)

            #return redirect("/profile/#/")
        else:
            #TODO Raise validation error
            print("invalid shit")
            print(form.is_valid())
            return HttpResponse("Registration error")
    elif request.method == 'OPTIONS':
        response = HttpResponse()
        response['allow'] = ','.join(['POST','OPTIONS'])
        return response
