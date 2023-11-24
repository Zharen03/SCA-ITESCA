from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import *

#Tests

def isAdministradorTest(user):
    grupo_admin = Group.objects.filter(name="Administrador").get()
    return grupo_admin in user.groups.all()

def isJefeDeDepartamentoTest(user):
    grupo_jefeDepartamento = Group.objects.filter(name="JefeDeDepartamento").get()
    return grupo_jefeDepartamento in user.groups.all()

#Views

def loginView(request):
    if request.user.is_authenticated:
            if isAdministradorTest(request.user):
                return redirect('../sca/show_user')
            else: 
                return redirect('../sca/show_invitations')
    failed_login = ""
    next = ""
    if "p" in request.GET.keys():
        failed_login = request.GET["p"]
    if "next" in request.GET.keys():
        next = request.GET["next"]
    template = loader.get_template('login.html')
    context = {"failed": failed_login,
               "next": next}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def loginAuth(request):
    next = request.GET["next"]
    print(request.POST)
    payroll_number = request.POST['payroll_number']
    password = request.POST['password']
    user = authenticate(request, username=payroll_number, password=password)
    if user is not None:
        login(request, user)
        if not next == "":
            return redirect(f'..{next}')
        if user.is_authenticated:
            if isAdministradorTest(user):
                return redirect('../sca/show_user')
            else: 
                return redirect('../sca/show_invitations')
    else:
        print(user, payroll_number, password)
    return redirect(f'../sca/login?p=invalid&next={next}')

def logoutUser(request):
    logout(request)
    
    return redirect('../sca/login')

@login_required
def showUser(request):
    users = User.objects.all().values()
    template = loader.get_template('show_users.html')
    print(request.user)
    context = {
        'users_list': users,
    }
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(isAdministradorTest)
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
    
    new_user = User.objects.create_user(post['payroll_number'], post["email"], post['password'], payroll_number = post['payroll_number'], 
                                        first_name = post["first_name"], last_name = post["last_name"], 
                                        phone_number = post["phone_number"], min_gender = False, min_general = False, role = int(post["type"]),
                                        area_id = area)                                                                                             
                    #payroll_number = post['payroll_number'], password = post['password'], position = post["position"], 
                    #first_name = post["first_name"], last_name = post["last_name"], email= post["email"], 
                    #phone_number = post["phone_number"], min_gender = False, min_general = False, role = int(post["type"]), 
                    #status = 1, area_id = area)
    print(new_user)
    new_user.groups.add(int(post["type"]))
    new_user.save()
    return HttpResponse("OK")


@csrf_exempt
def addDNC(request):
    post = request.POST
    print(post)
    new_DNC = DNC(user_id = post['user'], question_id = post['questions[0].question_id'], 
                  answer = post['questions[0].answer'], status = True)
    new_DNC.save()
    return HttpResponse("OK")
    
@login_required    
def trainingEventEvaluationSummaryForm(request):
    template = loader.get_template('training_event_evaluation_summary.html')
    context = {} 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def trainingEventEvaluationSummary(request):
    post = request.POST
    print(post)
    

@login_required
def trainingEventEvaluationForm(request):
    template = loader.get_template('training_event_evaluation.html')
    context = {}
    return HttpResponse(template.render(context, request))



@csrf_exempt
def trainingEventEvaluation(request):
    
    #TEMPORAL
    
    #FIN TEMPORAL
    
    evaluation_type = 0
    post = request.POST
    print(post)
    
    evaluation = Evaluation(type = evaluation_type )
    
    return HttpResponse("OK") 


@login_required
def virtualTrainingEventEvaluationForm(request):
    template = loader.get_template('virtual_training_event_evaluation.html')
    context = {} 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def virtualTrainingEventEvaluation(request):
    post = request.POST
    print(post)
    

@login_required
def showDNC(request):
    template = loader.get_template('show_dnc.html')
    context = {} 
    return HttpResponse(template.render(context, request))


@login_required
def trainingNeedsRequestForm(request):
    template = loader.get_template('needs_request.html')
    context = {} 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def trainingNeedsRequest(request):
    post = request.POST
    print(post)
    
    
@login_required
def showInvitations(request):
    template = loader.get_template('show_invitations.html')
    context = {} 
    return HttpResponse(template.render(context, request))
  
@login_required
def addTrainingForm(request):
    template = loader.get_template('add_training.html')
    context = {} 
    return HttpResponse(template.render(context, request))

@login_required
def evaluations(request):
    template = loader.get_template('evaluations.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def certificatesNoAdmin(request):
    template = loader.get_template('certificates_no_admin.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def show_attendances(request):
    template = loader.get_template('show_attendances.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def show_records(request):
    template = loader.get_template('show_records.html')
    context = {}
    return HttpResponse(template.render(context, request))
  
@login_required
def trainingHistoryNoAdmin(request):
    template = loader.get_template('training_history_no_admin.html')
    context = {} 
    return HttpResponse(template.render(context, request))

@login_required
def trainingHistoryAdmin(request):
    template = loader.get_template('training_history_admin.html')
    context = {} 
    return HttpResponse(template.render(context, request))

@login_required
def trainingPlan(request):
    template = loader.get_template('training_plan.html')
    context = {} 
    return HttpResponse(template.render(context, request))

@login_required
def showSummary(request):
    template = loader.get_template('show_summary.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def capacitationNeedsDetectionForm(request):
    template = loader.get_template('capacitation_needs_detection.html')
    context = {}
    return HttpResponse(template.render(context, request))
  
@login_required
def createWorkplan(request):
    template = loader.get_template('create_workplan.html')
    context = {} 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def addArea(request):
    try:
        # id=5 .delete()
        
        is_registered = Area.objects.filter(name=request.GET["name"])
        if len(is_registered) == 0 and request.GET["name"] is not None:
            new_area = Area(name=request.GET["name"])
            new_area.save()
        else:
            return HttpResponse("Ya fue registrado")
    except:
        return HttpResponse("Something gone wrong")
    return HttpResponse("ok")


def addGroup(request):
    
    #group = Group.objects.get(name='Administrador')
    #print(group.user_set)
    #try:
        #is_registered = Group.objects.filter(name=request.GET["name"])
        #if len(is_registered) == 0 and request.GET["name"] is not None:
            #new_group = Group(name=request.GET["name"])
            #new_group.save()
        #else:
            #return HttpResponse("Ya fue registrado")
    #except:
        #print(Group.objects.all())
        #return HttpResponse("Something gone wrong")
    return HttpResponse("ok")

