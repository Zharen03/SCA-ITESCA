from django.urls import path
from . import views

urlpatterns = [
    path('sca/add_user_form', views.addUserForm, name='add_user_form'),
    path('sca/add_user', views.addUser, name="add_user"),
    path('sca/show_user', views.showUser, name='show_user'),
    path('sca/show_dnc', views.showDNC, name='show_dnc'),
    path('sca/resume_training_events', views.trainingEventEvaluationSummaryForm, name='resume_training_events'),
    path('sca/training_events', views.trainingEventEvaluationForm, name='training_events'),
    path('sca/virtual_training', views.virtualTrainingEventEvaluationForm, name='virtual_training'),
    path('sca/show_invitations', views.showInvitations, name='show_invitations'),
    path('sca/training_needs_request', views.trainingNeedsRequestForm, name='training_needs_request'),
]