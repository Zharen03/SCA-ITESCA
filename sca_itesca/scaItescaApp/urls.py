from django.urls import path
from . import views

urlpatterns = [
    path('sca/add_user_form', views.addUserForm, name='add_user_form'),
    path('sca/add_user', views.addUser, name="add_user"),
    path('sca/show_user', views.showUser, name='show_user'),
    path('sca/resume_training_events', views.resume_training, name='resume_training_events'),
    path('sca/training_events', views.training_events, name='training_events'),
    path('sca/virtual_training', views.virtual_training, name='virtual_training'),
    path('sca/show_invitations', views.showInvitations, name='show_invitations'),
]