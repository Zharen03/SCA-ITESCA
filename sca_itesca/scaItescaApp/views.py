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
    position = post["position"]
    if position == "Por definir":
        position = 1
    
    
    new_user = User(payroll_number = post['payroll_number'], password = post['password'], position = post["position"], 
                    first_name = post["first_name"], last_name = post["last_name"], email= post["email"], phone_number = post["phone_number"],
                    min_gender = False, min_general = False, role = 1, status = 1)
    new_user.save()
    