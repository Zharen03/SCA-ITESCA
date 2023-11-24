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
    i = 0
    for a in range(8):
        new_DNC = DNC(user_id = post['user'], question_id = post[f"questions[{i}].question_id"], 
                  answer = post[f"questions[{i}].answer"], status = True)
        new_DNC.save()
        i = i+1
        
    return HttpResponse("OK")

 
@csrf_exempt   
def addNeedsRequest(request):
    post = request.POST
    print(post)
    i=0
    for a in range(8):
        new_needs_request = Needs_Request(user_id = post['user'], question_id=post[f"questions[{i}].question_id"],
                                          answer = post[f"questions[{i}].answer"], status=post["status"])
        new_needs_request.save()
        i = i+1

@csrf_exempt
def addTraining(request):
    post = request.POST
    new_training = Training(name = post['name'], description=post['description'], attendance_code=post['attendance_code'], 
                            modality=post['modality'], general=post['general'], internal=post['internal'], 
                            status=post['status'], area_id=post['area_id'])
    new_training.save()
    
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
    evaluations = Evaluation.objects.all().values()


    template = loader.get_template('evaluations.html')
    context = {"evaluations": evaluations}
    return HttpResponse(template.render(context, request))

@login_required
def certificatesNoAdmin(request):
    template = loader.get_template('certificates_no_admin.html')
    context = {}
    return HttpResponse(template.render(context, request))

  
class showAttendance:
    def __init__(self, name, attendance):
        self.name = name
        self.attendance = attendance
  
  
@login_required
def show_attendances(request):
    #This will be the variable that holds the user id account
    userID = ""

    #Bring user table obj
    user = User.objects.all().values()

    #Variable for user name
    name
    #Variable for attendance
    attendance
    
    #Variable that holds objects
    objList

    user_training = User_Training.objects.all().values()
    
    for u in user:
        if (u.payroll_number == userID):
            name = u.first_name
            for ut in user_training:
                if (ut.user_id == u.payroll_number):
                    attendance = ut.attendance
                    p = showAttendance(name, attendance)
                    objList.append(p)
            
    


    template = loader.get_template('show_attendances.html')
    context = {"userTraining": objList}
    return HttpResponse(template.render(context, request))

@login_required
def show_records(request):
    template = loader.get_template('show_records.html')
    context = {}
    return HttpResponse(template.render(context, request))
 
class training_h_na:
    def __init__(self, name, date, type, attendance):
        self.name = name
        self.date = date
        self.type = type
        self.attendace = attendance


@login_required
def trainingHistoryNoAdmin(request):
    #This will be the variable that holds the user id account
    userID = ""

    #Bring training table obj
    training = Training.objects.all().values()
    #Bring date training table obj
    date_training = Date_Training.objects.all().values()
    #Bring date table obj
    date = Date.objects.all().values()
    #Bring user_training
    user_training = User_Training.objects.all().values()

    #Variable that will hold us nombre fecha tipo asistencia
    training_Name
    #Variable that holds date training
    training_Date
    #Variable that holds type training
    training_Type
    #Variable that holds attendance
    training_Attendance

    #This variable will hold the list for objects for the table
    objList

    for user in user_training:
        if (user.user_id == userID):
            if (user.attendace):
                training_Attendance = "Asistio"
            else:
                training_Attendance = "No asistio"
            for t in training:
                if (user.training_id == t.ID):
                    training_Name = t.name
                    if (t.general):
                        training_Type = "General"
                    if (t.internal):
                        training_Type = "Interno"
                    for dt in date_training:
                        if (t.ID == dt.training_id):
                            for d in date:
                                if (dt.training_id == d.ID):
                                    training_Date = str(d.day) + str(d.month) + str(d.year)
                                    p = training_h_na(training_Name, training_Date, training_Type, training_Attendance)
                                    objList.append(p)
   



    template = loader.get_template('training_history_no_admin.html')
    context = {'training_na_list': objList} 
    return HttpResponse(template.render(context, request))

@login_required
def trainingHistoryAdmin(request):
    #This will be the variable that holds the user id account
    userID = ""

    #Bring training table obj
    training = Training.objects.all().values()
    #Bring date training table obj
    date_training = Date_Training.objects.all().values()
    #Bring date table obj
    date = Date.objects.all().values()
    #Bring user_training
    user_training = User_Training.objects.all().values()

    #Variable that will hold us nombre fecha tipo asistencia
    training_Name
    #Variable that holds date training
    training_Date
    #Variable that holds type training
    training_Type
    #Variable that holds attendance
    training_Attendance

    #This variable will hold the list for objects for the table
    objList

    for user in user_training:
        if (user.user_id == userID):
            if (user.attendace):
                training_Attendance = "Asistio"
            else:
                training_Attendance = "No asistio"
            for t in training:
                if (user.training_id == t.ID):
                    training_Name = t.name
                    if (t.general):
                        training_Type = "General"
                    if (t.internal):
                        training_Type = "Interno"
                    for dt in date_training:
                        if (t.ID == dt.training_id):
                            for d in date:
                                if (dt.training_id == d.ID):
                                    training_Date = str(d.day) + str(d.month) + str(d.year)
                                    p = training_h_na(training_Name, training_Date, training_Type, training_Attendance)
                                    objList.append(p)



    template = loader.get_template('training_history_admin.html')
    context = {'training_ad_list': objList,} 
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

  
def update_user(request):
    template = loader.get_template('update_user.html')
    context = {} 
    return HttpResponse(template.render(context, request))


def certificates_admin(request):
    template = loader.get_template('certificates_admin.html')
    context = {} 
    return HttpResponse(template.render(context, request))


def records_module(request):
    template = loader.get_template('records_module.html')
    context = {} 
    return HttpResponse(template.render(context, request))


def certificate_review(request):
    template = loader.get_template('certificate_review.html')
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

