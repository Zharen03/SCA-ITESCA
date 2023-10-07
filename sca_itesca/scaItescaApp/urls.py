from django.urls import path
from . import views

urlpatterns = [
    path('sca/add_user_form', views.addUserForm, name='add_user_form'),
    path('sca/add_user', views.addUser, name="add_user"),
    path('sca/show_user', views.showUser, name='show_user'),
    
]