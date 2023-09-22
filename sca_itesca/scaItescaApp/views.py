from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.utils.encoding import smart_str

# Create your views here.

#View to add user to the platform
def add_user_template(request):
    #Opening the html document that contains the template
    extern_template = open("../sca_itesca/scaItescaApp/templates/add_user_form.html")
    #Loading the template in a template type variable
    template = Template(extern_template.read())
    #Close the document that was opened before
    extern_template.close()
    #Creating the context for the template
    context = Context()
    #Render the template
    document = template.render(context)

    return HttpResponse(document)