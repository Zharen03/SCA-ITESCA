from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import * 

def showUser(request):
    users = User.objects.all().values()
    
    template = loader.get_template('addUser.html')    
    context = {
        'users_list': users
    }
    #return HttpResponse(template.render(context, request))
    return HttpResponse("showuser")

def addUser(request):
    post = request.POST
    
    new_user = User(user_name = post['user_name'])
    new_user.save()
    
    return HttpResponse("addUser")