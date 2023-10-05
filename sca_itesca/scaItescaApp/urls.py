from django.urls import path
from . import views

urlpatterns = [
    path('sca/add_user_form', views.addUserForm, name='add_user_form'),
]