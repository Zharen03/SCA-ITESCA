from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import *
import datetime

#Tests

def isAdministradorTest(user):
    grupo_admin = Group.objects.filter(name="Administrador").get()
    return grupo_admin in user.groups.all()

def isJefeDeDepartamentoTest(user):
    grupo_jefeDepartamento = Group.objects.filter(name="JefeDeDepartamento").get()
    return grupo_jefeDepartamento in user.groups.all()

def userTypeTest(user):
    if isAdministradorTest(user):
        return "Administrador"
    if isJefeDeDepartamentoTest(user):
        return "Jefe de departamento"
    return "Personal"

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
@csrf_exempt
def showUser(request):
    users = User.objects.all()
    if "input_name" in request.POST.keys():
        if not request.POST["input_name"] == "":
            users = users.filter(first_name=request.POST["input_name"])
    else:
        users = users.values()
    template = loader.get_template('show_users.html')
    context = {
        'users_list': users,
        'user_type': userTypeTest(request.user),
    }
    return HttpResponse(template.render(context, request))


def addUserForm(request):
    template = loader.get_template('add_user_form.html')
    areas = Area.objects.all().values()    
    context = {
        "areas": areas,
        'user_type': userTypeTest(request.user),
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def addUser(request):
    post = request.POST
    print(post)
    area = Area.objects.filter(id=int(post["area"]))[0]
    print(area)
    
    new_user = User.objects.create_user(post['payroll_number'], post["email"], post['password'], payroll_number = post['payroll_number'], 
                                        first_name = post["first_name"], last_name = post["last_name"], position = post["position"],
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

def trainingHistoryRedirect(request):
    if isAdministradorTest(request.user):
        return redirect("../sca/training_history_ad")
    return redirect("../sca/training_history_na")
        

@csrf_exempt
def addTraining(request):
    post = request.POST
    obj_area = Area.objects.filter(id=post["area_id"])[0]
    new_training = Training(name = post['name'], trainer=post["trainer"], description=post['description'], attendance_code=post['attendance_code'], 
                            modality=(post['modality']=="true"), general=(post['general']=="true"), internal=(post['internal']=="true"), 
                            status=1, area_id=obj_area)
    new_training.save()
    raw_date = request.POST["date"].split("-")
    raw_time = request.POST["time"].split(":")
    
    print(raw_date, raw_time)
    date = datetime.date(int(raw_date[0]), int(raw_date[1]), int(raw_date[2]))
    time = datetime.time(hour=int(raw_time[0]), minute=int(raw_time[1]))
    dates = Date.objects.all()
    bool_date = False
    for obj_date in dates:
        if date == obj_date.day:
            bool_date = True
    if not bool_date:
        new_date = Date(day=date)
        new_date.save()
    obj_date = Date.objects.filter(day = date)[0]
    new_date_training = Date_Training(training_id=new_training, date_id=obj_date, time=time)
    new_date_training.save()
    
    new_invitation = Invitation(training_id=new_training, description=post["description"], optional=(post["optional"]=="Publica"))
    new_invitation.save()
    
    for user in User.objects.filter(area_id=request.POST["area_id"]):
        new_user_invitation = User_Invitation(user_id=user, invitation_id=new_invitation, status=2, visible=1)
        new_user_invitation.save()
    return HttpResponse("ok")
    

@login_required    
def trainingEventEvaluationSummaryForm(request):
    template = loader.get_template('training_event_evaluation_summary.html')
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def trainingEventEvaluationSummary(request):
    post = request.POST
    print(post)
    

@login_required
def trainingEventEvaluationForm(request):
    template = loader.get_template('training_event_evaluation.html')
    context = {
        'user_type': userTypeTest(request.user),
    }
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
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def virtualTrainingEventEvaluation(request):
    post = request.POST
    print(post)
    

@login_required
def showDNC(request):
    template = loader.get_template('show_dnc.html')
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))


@login_required
def trainingNeedsRequestForm(request):
    template = loader.get_template('needs_request.html')
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def trainingNeedsRequest(request):
    post = request.POST
    print(post)
    
    
@login_required
def showInvitations(request):
    template = loader.get_template('show_invitations.html')
    user_invitation = User_Invitation.objects.filter(user_id=request.user)
    print(user_invitation)
    invitation_list = []
    for invitation in user_invitation:
        obj_invitation = Invitation.objects.filter(id=invitation.invitation_id.id)[0]
        print(obj_invitation)
        obj_training = Training.objects.filter(id=obj_invitation.training_id.id)[0]
        obj_date_training = Date_Training.objects.filter(training_id=obj_training)
        date_list = []
        for date in obj_date_training:
            obj_date = Date.objects.filter(id=date.date_id.id)[0]
            date_list.append({"date":obj_date.day, "time":date.time})
        invitation_list.append({"invitation_info":obj_invitation, "relation":invitation, "training_info":obj_training, "schedule": date_list})
    context = {
            "invitation_list": invitation_list,
            'user_type': userTypeTest(request.user),
        }
    print(invitation_list)
    return HttpResponse(template.render(context, request))
  
@login_required
def addTrainingForm(request):
    template = loader.get_template('add_training.html')
    areas = Area.objects.all().values()
    context = {
        "areas":areas,
        'user_type': userTypeTest(request.user),
        } 
    return HttpResponse(template.render(context, request))

@login_required
def evaluations(request):
    evaluations = Evaluation.objects.all().values()


    template = loader.get_template('evaluations.html')
    context = {
        "evaluations": evaluations,
        'user_type': userTypeTest(request.user),
        }
    return HttpResponse(template.render(context, request))

@login_required
def certificatesNoAdmin(request):
    template = loader.get_template('certificates_no_admin.html')
    context = {
        'user_type': userTypeTest(request.user),
    }
    return HttpResponse(template.render(context, request))

  
class showAttendance:
    def __init__(self, name, attendance):
        self.name = name
        self.attendance = attendance
  
  
@login_required
def show_attendances(request):
    #This will be the variable that holds the user id account
    userID = request.user.payroll_number

    #Bring user table obj
    user = User.objects.all()

    #Variable for user name
    name = ""
    #Variable for attendance
    attendance = ""
    
    #Variable that holds objects
    objList = []

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
    context = {
        "userTraining": objList,
        'user_type': userTypeTest(request.user),
    }
    return HttpResponse(template.render(context, request))

@login_required
def show_records(request):
    template = loader.get_template('show_records.html')
    context = {
        'user_type': userTypeTest(request.user),
    }
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
    userID = request.user.payroll_number

    #Bring training table obj
    training = Training.objects.all().values()
    #Bring date training table obj
    date_training = Date_Training.objects.all().values()
    #Bring date table obj
    date = Date.objects.all().values()
    #Bring user_training
    user_training = User_Training.objects.all().values()

    #Variable that will hold us nombre fecha tipo asistencia
    training_Name = ""
    #Variable that holds date training
    training_Date = ""
    #Variable that holds type training
    training_Type = ""
    #Variable that holds attendance
    training_Attendance = ""

    #This variable will hold the list for objects for the table
    objList = []

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
    context = {
        'training_na_list': objList,
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))

@login_required
def trainingHistoryAdmin(request):
    #This will be the variable that holds the user id account
    userID = request.user.payroll_number

    #Bring training table obj
    training = Training.objects.all().values()
    #Bring date training table obj
    date_training = Date_Training.objects.all().values()
    #Bring date table obj
    date = Date.objects.all().values()
    #Bring user_training
    user_training = User_Training.objects.all()

    #Variable that will hold us nombre fecha tipo asistencia
    training_Name = ""
    #Variable that holds date training
    training_Date = ""
    #Variable that holds type training
    training_Type =""
    #Variable that holds attendance
    training_Attendance = ""

    #This variable will hold the list for objects for the table
    objList = []

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
    context = {
        'training_ad_list': objList,
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))

@login_required
def trainingPlan(request):
    template = loader.get_template('training_plan.html')
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))

@login_required
def showSummary(request):
    template = loader.get_template('show_summary.html')
    context = {
        'user_type': userTypeTest(request.user),
    }
    return HttpResponse(template.render(context, request))

@login_required
def capacitationNeedsDetectionForm(request):
    template = loader.get_template('capacitation_needs_detection.html')
    context = {
        'user_type': userTypeTest(request.user),
    }
    return HttpResponse(template.render(context, request))
  
@login_required
def createWorkplan(request):
    template = loader.get_template('create_workplan.html')
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))

def pass_recovery(request):
    template = loader.get_template('pass_recovery.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
  
def update_user(request):
    template = loader.get_template('update_user.html')
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))


def certificates_admin(request):
    template = loader.get_template('certificates_admin.html')
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))


def records_module(request):
    template = loader.get_template('records_module.html')
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))


def certificate_review(request):
    template = loader.get_template('certificate_review.html')
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))
  

@csrf_exempt
def addArea(request):
    try:
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
    try:
        is_registered = Group.objects.filter(name=request.GET["name"])
        if len(is_registered) == 0 and request.GET["name"] is not None:
            new_group = Group(name=request.GET["name"])
            new_group.save()
        else:
            return HttpResponse("Ya fue registrado")
    except:
        print(Group.objects.all())
        return HttpResponse("Something gone wrong")
    return HttpResponse("ok")
