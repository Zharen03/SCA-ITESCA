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



def addUserForm(request):
    template = loader.get_template('add_user_form.html')    
    context = {
        
    }
    
    return HttpResponse(template.render(context, request))

def addUser(request):
    post = request.POST
    
    new_user = User(user_name = post['user_name'])
    new_user.save()

def resume_training (request): 
    template = loader.get_template('resume_training_events.html')    
    context = {
        
    }
    
    return HttpResponse(template.render(context, request))

def training_events (request): 
    template = loader.get_template('training_events.html')    
    context = {
        
    }
    
    return HttpResponse(template.render(context, request))

def virtual_training (request): 
    template = loader.get_template('virtual_training.html')    
    context = {
        
    }
    
    return HttpResponse(template.render(context, request))
    