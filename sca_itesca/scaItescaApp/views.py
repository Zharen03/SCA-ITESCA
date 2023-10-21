from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import loader
from .models import *

def showUser(request):
    users = User.objects.all().values()
    template = loader.get_template('show_users.html')    
    context = {
        'users_list': users
    }
    return HttpResponse(template.render(context, request))


def addUserForm(request):
    template = loader.get_template('add_user_form.html')
    areas = Area.objects.all().values()    
    context = {
        "areas": areas
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def addUser(request):
    post = request.POST
    print(post)
    area = Area.objects.filter(id=int(post["area"]))[0]
    print(area)
    
    new_user = User(payroll_number = post['payroll_number'], password = post['password'], position = post["position"], 
                    first_name = post["first_name"], last_name = post["last_name"], email= post["email"], 
                    phone_number = post["phone_number"], min_gender = False, min_general = False, role = int(post["type"]), 
                    status = 1, area_id = area)
    new_user.save()
    return HttpResponse("OK")
    
    
def trainingEventEvaluationSummaryForm(request):
    template = loader.get_template('training_event_evaluation_summary.html')
    context = {} 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def trainingEventEvaluationSummary(request):
    post = request.POST
    print(post)
    

def trainingEventEvaluationForm(request):
    template = loader.get_template('training_event_evaluation.html')
    context = {} 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def trainingEventEvaluation(request):
    post = request.POST
    print(post)


def virtualTrainingEventEvaluationForm(request):
    template = loader.get_template('virtual_training_event_evaluation.html')
    context = {} 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def virtualTrainingEventEvaluation(request):
    post = request.POST
    print(post)
    
    
def showDNC(request):
    template = loader.get_template('show_dnc.html')
    context = {} 
    return HttpResponse(template.render(context, request))


def trainingNeedsRequestForm(request):
    template = loader.get_template('needs_request.html')
    context = {} 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def trainingNeedsRequest(request):
    post = request.POST
    print(post)
    
    
def showInvitations(request):
    template = loader.get_template('show_invitations.html')
    context = {} 
    return HttpResponse(template.render(context, request))


def trainingPlan(request):
    template = loader.get_template('training_plan.html')
    context = {} 
    return HttpResponse(template.render(context, request))

