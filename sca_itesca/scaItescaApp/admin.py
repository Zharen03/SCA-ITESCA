from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from .models import *



# Register your models here.
admin.site.register(User, UserAdmin)

#Resource
class UserResource(resources.ModelResource):
    
    class Meta:
        model = User
        fields = ("payroll_number", "first_name", "last_name", "email", "phone_number", "position", "min_gender", "min_general", "is_active") 
    
    def dehydrate_min_gender(self, user):
        user_min_gender = getattr(user, "min_gender", "unkown")
        if user_min_gender:
            return "Realizado"
        else:
            return "No realizado"
        
    def dehydrate_min_general(self, user):
        user_min_general = getattr(user, "min_general", "unkown")
        if user_min_general:
            return "Realizado"
        else:
            return "No realizado"
        
    def dehydrate_is_active(self, user):
        user_is_active = getattr(user, "is_active", "unkown")
        if user_is_active:
            return "Activo"
        else:
            return "Inactivo"

class CapacitationResource(resources.ModelResource):
    class Meta:
        model = Training
        #fields = ("name", "trainer", "modality") 

class EvaluationsResource(resources.ModelResource):
    class Meta:
        
        model = Evaluation
        #fields = ("user_id", "status") 
        
class DNCResource(resources.ModelResource):
    class Meta:
        
        model = Evaluation
        fields = ("user_id", "done") 