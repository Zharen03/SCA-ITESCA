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
from http import HTTPStatus
from .forms import *

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

#Login module views



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


def pass_recovery(request):
    template = loader.get_template('pass_recovery.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


#User module views

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
    areas = Area.objects.all().values()
    trainings = Training.objects.all().values()
    context = {
        'users_list': users,
        'user_type': userTypeTest(request.user),
        'areas':areas,
        'trainings':trainings,
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


def update_user(request):
    template = loader.get_template('update_user.html')
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))


#DNC module views
@login_required
def capacitationNeedsDetectionForm(request):
    template = loader.get_template('capacitation_needs_detection.html')
    context = {
        'user_type': userTypeTest(request.user),
    }
    return HttpResponse(template.render(context, request))

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


@login_required
def showDNC(request):
    template = loader.get_template('show_dnc.html')
    context = {
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))

 
#Needs request module views
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
    

#Trainings module views

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
    
    users = User.objects
    if post["optional"]=="Publica":
        users = users.all()
    else:
        users = users.filter(area_id=request.POST["area_id"])
        
    for user in users:
        new_user_invitation = User_Invitation(user_id=user, invitation_id=new_invitation, status=2, visible=1)
        new_user_invitation.save()
        if post["optional"] == "Obligatoria":
            new_user_training = User_Training(training_id=new_training, user_id=user,
                                                attendance=False, certified=False)
            new_user_training.save()
            
            if new_training.modality:
                new_evaluation = Evaluation(type=0, training_id=new_training, user_id=user, status=0)
                new_evaluation.save()
            else:
                new_vitrual_evaluation = Evaluation(type=1, training_id=new_training, user_id=user, status=0)
                new_vitrual_evaluation.save()
    return HttpResponse(new_training.id)
    
@csrf_exempt
def uploadFile(request):
    #for file in request.POST["file"]:
        #print("que", file)
    #print("so")
    return HttpResponse("ok")


@login_required
def addTrainingForm(request):
    template = loader.get_template('add_training.html')
    areas = Area.objects.all().values()
    form = FileForm()
    context = {
        "areas":areas,
        'user_type': userTypeTest(request.user),
        "form":form
        } 
    return HttpResponse(template.render(context, request))


@login_required
def trainingHistoryNoAdmin(request):
    training_list = []
    
    trainings = User_Training.objects.filter(user_id= request.user)
    for training in trainings:
        obj_training = Training.objects.filter(id=training.training_id.id)[0]
        dates = Date_Training.objects.filter(training_id = obj_training)
        obj_date = []
        for date in dates:
            obj_date.append(Date.objects.filter(id=date.date_id.id)[0])
        training_list.append({"training": obj_training, "date": obj_date, "type":obj_training.modality, "attendance": training.attendance})
    
    template = loader.get_template('training_history_no_admin.html')
    context = {
        'training_na_list': training_list,
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))

@login_required
def trainingHistoryAdmin(request):
    training_list = []
    
    trainings = Training.objects.all()
    for training in trainings:
        dates = Date_Training.objects.filter(training_id = training)
        obj_date = []
        for date in dates:
            obj_date.append(Date.objects.filter(id=date.date_id.id)[0])
        training_list.append({"training": training, "date": obj_date, "type":training.modality})
    
    template = loader.get_template('training_history_admin.html')
    context = {
        'training_ad_list': training_list,
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))


#Evaluations module views
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
    eid = request.POST["evaluation_id"]
    evaluation_status = Evaluation.objects.filter(id=eid)[0]
    evaluation_status = evaluation_status.status
    
    template = loader.get_template('training_event_evaluation.html')
    context = {
        "e_status": evaluation_status,
        "eid":eid,
        'user_type': userTypeTest(request.user),
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def trainingEventEvaluation(request):
    post = request.POST
    
    evaluation = Evaluation.objects.filter(id=post["evaluation_id"])[0]
    post_keys = list(post.keys())
    for key in range(2, len(post_keys)-1):
        print(key)
        obj_question = Question.objects.filter(id=key-1)[0]
        new_evaluation_question = Evaluation_Question(evaluation_id=evaluation, question_id=obj_question, answer=post[post_keys[key]])
        new_evaluation_question.save()
    if not post["comments"] == "":
        obj_question = Question.objects.filter(id=13)[0]
        new_evaluation_question = Evaluation_Question(evaluation_id=evaluation, question_id=obj_question, answer=post[post_keys[key]])
        new_evaluation_question.save()
    evaluation.status = 1
    evaluation.save()    
    print(Evaluation_Question.objects.all().values())
    
    return redirect("/sca/evaluations_na")


@login_required
def virtualTrainingEventEvaluationForm(request):
    eid = request.POST["evaluation_id"]
    evaluation_status = Evaluation.objects.filter(id=eid)[0]
    evaluation_status = evaluation_status.status
    template = loader.get_template('virtual_training_event_evaluation.html')
    context = {
        "e_status": evaluation_status,
        "eid":eid,
        'user_type': userTypeTest(request.user),
    } 
    return HttpResponse(template.render(context, request))


@csrf_exempt
def virtualTrainingEventEvaluation(request):
    post = request.POST
    
    evaluation = Evaluation.objects.filter(id=post["evaluation_id"])[0]
    post_keys = list(post.keys())
    for key in range(2, len(post_keys)-1):
        print(key)
        obj_question = Question.objects.filter(id=key+12)[0]
        new_evaluation_question = Evaluation_Question(evaluation_id=evaluation, question_id=obj_question, answer=post[post_keys[key]])
        new_evaluation_question.save()
    if not post["comments"] == "":
        obj_question = Question.objects.filter(id=21)[0]
        new_evaluation_question = Evaluation_Question(evaluation_id=evaluation, question_id=obj_question, answer=post[post_keys[key]])
        new_evaluation_question.save()
    evaluation.status = 1
    evaluation.save()    
    print(Evaluation_Question.objects.all().values())
    return redirect("/sca/evaluations_na")


@login_required
def evaluations(request):
    
    trainings = Training.objects.filter(status=True) 
    
    template = loader.get_template('evaluations.html')
    context = {
        "trainings": trainings,
        'user_type': userTypeTest(request.user),
        }
    return HttpResponse(template.render(context, request))


@login_required
def showEvaluations(request, tid=0):
    obj_training = Training.objects.filter(id=tid)[0]
    evaluations = Evaluation.objects.filter(training_id=obj_training) 
    print(Evaluation.objects.all().values())
    template = loader.get_template('show_evaluations.html')
    context = {
        "evaluations": evaluations,
        'user_type': userTypeTest(request.user),
        }
    return HttpResponse(template.render(context, request))


@login_required
def evaluationsNoAdmin(request):
    user_trainings = User_Training.objects.filter(user_id= request.user)

    trainings = []
    for user_training in user_trainings:
        obj_training = user_training.training_id
        evaluations = Evaluation.objects.filter(training_id=obj_training)
        evaluations = evaluations.filter(user_id=request.user)
        if len(evaluations) > 0:
            evaluations = evaluations[0]
        else:
            evaluations = ""
        trainings.append({"training":obj_training, "evaluation":evaluations})
    
    template = loader.get_template('evaluations_na.html')
    context = {
        "trainings": trainings,
        'user_type': userTypeTest(request.user),
        }
    return HttpResponse(template.render(context, request))

@login_required 
def showSummary(request):
    #This is an evaluations page
    template = loader.get_template('show_summary.html')
    context = {
        'user_type': userTypeTest(request.user),
    }
    return HttpResponse(template.render(context, request))

#Invitations module views  
@login_required
def showInvitations(request):
    template = loader.get_template('show_invitations.html')
    user_invitation = User_Invitation.objects.filter(user_id=request.user)
    invitation_list = []
    for invitation in user_invitation:
        obj_invitation = Invitation.objects.filter(id=invitation.invitation_id.id)[0]
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
    return HttpResponse(template.render(context, request))


#Attendance module views
@csrf_exempt
def setAttendance(request):
    #ver tiempo
    #if request.method == 'POST':
    post = request.POST
    print(post)
    obj_training = Training.objects.filter(attendance_code=post["attendance_code"])
    if len(obj_training) > 0:
        user_training = User_Training.objects.filter(training_id=obj_training[0])
        user_training = user_training.filter(user_id=request.user)[0]
        user_training.attendance = True
        print(user_training)
        user_training.save()
    else:
        return HttpResponse(HTTPStatus.NOT_FOUND)
    return HttpResponse("ok")     
    
      
@login_required
def show_attendances(request, tid=1):
    
    obj_training = Training.objects.filter(id=tid)[0]
    user_training = User_Training.objects.filter(training_id=obj_training)
    
    attendance_list= []
    for user in user_training:
        obj_user = User.objects.filter(payroll_number=user.user_id.payroll_number)[0]
        attendance_list.append({
            "id":obj_user.payroll_number,
            "name":f"{obj_user.first_name} {obj_user.last_name}",
            "attendance": "Asistio" if user.attendance  else "No asistio"
        })
    print(attendance_list)
    template = loader.get_template('show_attendances.html')
    context = {
        "tid":tid,
        "attendance_list": attendance_list,
        'user_type': userTypeTest(request.user),
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def updateAttendance(request):
    post = request.POST
    print(post)
    obj_training = Training.objects.filter(id=post["training_id"])[0]
    obj_user = User.objects.filter(payroll_number=post["user_id"])[0]
    user_training = User_Training.objects.filter(training_id=obj_training)
    user_training = user_training.filter(user_id=obj_user)[0]
    if int(post["change"]) == 1:
        user_training.attendance = True
    else:
        user_training.attendance = False
    
    user_training.save()
    return HttpResponse("ok")


#Certificates module views
@login_required
def certificatesNoAdmin(request):
    template = loader.get_template('certificates_no_admin.html')
    context = {
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
  

#Training plan module views
@login_required
def trainingPlan(request):
    template = loader.get_template('training_plan.html')
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


#Extra modules

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


def addQuestion(request):
    get = request.GET
    
    q = Question(description=get["description"])
    q.save()
    return HttpResponse("ok")