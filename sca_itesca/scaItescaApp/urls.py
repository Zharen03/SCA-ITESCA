from django.urls import path
from . import views

urlpatterns = [
    path('sca/add_group', views.addGroup),
    path('sca/login', views.loginView, name="login"),
    path('sca/login_auth', views.loginAuth),
    path('sca/logout_user', views.logoutUser),
    
    path('sca/add_user_form', views.addUserForm, name='add_user_form'),
    path('sca/add_user', views.addUser, name="add_user"),
    path('sca/show_user', views.showUser, name='show_user'),
    path("sca/add_area", views.addArea, name="add_area"),
    
    path('sca/show_dnc', views.showDNC, name='show_dnc'),
    
    path('sca/resume_training_events', views.trainingEventEvaluationSummaryForm, name='resume_training_events'),
    path('sca/training_events_evaluation_form', views.trainingEventEvaluationForm, name='training_events'),
    path('sca/training_event_evaluation', views.trainingEventEvaluation, name='training_event_evaluation'),
    path('sca/virtual_training_event_evaluation', views.virtualTrainingEventEvaluation, name='virtual_training_event_evaluation'),
    path('sca/virtual_training_evemt_evaluation_form', views.virtualTrainingEventEvaluationForm, name='virtual_training'),
    path('sca/show_invitations', views.showInvitations, name='show_invitations'),
    path('sca/training_needs_request', views.trainingNeedsRequestForm, name='training_needs_request'),
    path('sca/add_training', views.addTrainingForm, name="add_training"),
    path('sca/training_history_na', views.trainingHistoryNoAdmin, name="training_history_na"),
    path('sca/training_history_ad', views.trainingHistoryAdmin, name="training_history_ad"),
    path('sca/training_plan', views.trainingPlan, name="training_plan"),
    path('sca/show_summary', views.showSummary, name="show_summary"),
    path('sca/capacitation_needs_detection', views.capacitationNeedsDetectionForm, name="capacitation_needs_detection"),
    path('sca/add_dnc', views.addDNC, name='add_dnc'),
    path('sca/training_needs_request_form', views.trainingNeedsRequestForm, name='training_needs_request'),
    path('sca/training_needs_request', views.trainingNeedsRequest, name='training_needs'),
    path('sca/create_workplan', views.createWorkplan, name='create_workplan'),
    path('sca/evaluations', views.evaluations, name="evaluations"),
    path('sca/certificates', views.certificatesNoAdmin, name="certificates_no_admin"),
    path('sca/show_records', views.show_records, name="show_records"),
    path('sca/show_attendances', views.show_attendances, name="show_attendances"),
]