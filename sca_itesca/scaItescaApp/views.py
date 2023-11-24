from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import loader
from .models import *

def login(request):
    template = loader.get_template('login.html')    
    context = {}
    return HttpResponse(template.render(context, request))


def showUser(request):
    users = User.objects.all().values()
    template = loader.get_template('show_users.html')    
    context = {
        'users_list': users,
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

  
@csrf_exempt
def addDNC(request):
    post = request.POST
    print(post)
    new_DNC = DNC(user_id = post['user'], question_id = post['questions[0].question_id'], 
                  answer = post['questions[0].answer'], status = True)
    new_DNC.save()
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
    
    #TEMPORAL
    
    #FIN TEMPORAL
    
    evaluation_type = 0
    post = request.POST
    print(post)
    
    evaluation = Evaluation(type = evaluation_type )
    
    return HttpResponse("OK") 


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
  
  
def addTrainingForm(request):
    template = loader.get_template('add_training.html')
    context = {} 
    return HttpResponse(template.render(context, request))

  
def evaluations(request):
    evaluations = Evaluation.objects.all().values()


    template = loader.get_template('evaluations.html')
    context = {"evaluations": evaluations}
    return HttpResponse(template.render(context, request))

  
def certificatesNoAdmin(request):
    template = loader.get_template('certificates_no_admin.html')
    context = {}
    return HttpResponse(template.render(context, request))

class showAttendance:
    def __init__(self, name, attendance):
        self.name = name
        self.attendance = attendance
  
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

  
def trainingPlan(request):
    template = loader.get_template('training_plan.html')
    context = {} 
    return HttpResponse(template.render(context, request))

  
def showSummary(request):
    template = loader.get_template('show_summary.html')
    context = {}
    return HttpResponse(template.render(context, request))

  
def capacitationNeedsDetectionForm(request):
    template = loader.get_template('capacitation_needs_detection.html')
    context = {}
    return HttpResponse(template.render(context, request))
  
  
def createWorkplan(request):
    template = loader.get_template('create_workplan.html')
    context = {} 
    return HttpResponse(template.render(context, request))
