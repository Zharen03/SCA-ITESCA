from django.urls import path
from . import views

urlpatterns = [
    path("sca/add_question", views.addQuestion, name="add_question"),
    path("sca/add_area", views.addArea, name="add_area"),
    path('sca/add_group', views.addGroup),
    path('sca/login', views.loginView, name="login"),
    path('sca/login_auth', views.loginAuth),
    path('sca/logout_user', views.logoutUser),
    path('sca/pass_recovery', views.pass_recovery, name="pass_recovery"),
    
    path('sca/add_user_form', views.addUserForm, name='add_user_form'),
    path('sca/add_user', views.addUser, name="add_user"),
    path('sca/add_training_form', views.addTrainingForm, name="add_training_form"),
    path('sca/add_training', views.addTraining, name="add_training"),
    path('sca/add_dnc', views.addDNC, name='add_dnc'),
    path('sca/add_needs_request', views.addNeedsRequest, name='add_needs_request'),
    
    path('sca/show_user', views.showUser, name='show_user'),
    path('sca/show_dnc', views.showDNC, name='show_dnc'),
    path('sca/show_invitations', views.showInvitations, name='show_invitations'),
    path('sca/show_records', views.show_records, name="show_records"),
    path('sca/show_attendances/<int:tid>/', views.show_attendances, name="show_attendances"),
    path('sca/show_evaluations/<int:tid>/', views.showEvaluations, name="show_evaluations"),
    path('sca/evaluations', views.evaluations, name="evaluations"),
    path('sca/evaluations_na', views.evaluationsNoAdmin, name="evaluations_na"),
    path('sca/certificates', views.certificatesNoAdmin, name="certificates_no_admin"),
    path('sca/certificates_admin', views.certificates_admin, name="certificates_admin"),
    
    path('sca/resume_training_events', views.trainingEventEvaluationSummaryForm, name='resume_training_events'),
    path('sca/training_events_evaluation_form', views.trainingEventEvaluationForm, name='training_events'),
    path('sca/training_event_evaluation', views.trainingEventEvaluation, name='training_event_evaluation'),
    path('sca/virtual_training_event_evaluation', views.virtualTrainingEventEvaluation, name='virtual_training_event_evaluation'),
    path('sca/virtual_training_event_evaluation_form', views.virtualTrainingEventEvaluationForm, name='virtual_training'),
    path('sca/show_summary', views.showSummary, name="show_summary"),
    path('sca/capacitation_needs_detection', views.capacitationNeedsDetectionForm, name="capacitation_needs_detection"),
    path('sca/training_needs_request_form', views.trainingNeedsRequestForm, name='training_needs_request'),
    path('sca/training_needs_request', views.trainingNeedsRequest, name='training_needs'),
    
    path('sca/training_history_redirect', views.trainingHistoryRedirect, name="training_history_r"),
    path('sca/training_history_na', views.trainingHistoryNoAdmin, name="training_history_na"),
    path('sca/training_history_ad', views.trainingHistoryAdmin, name="training_history_ad"),
    path('sca/training_plan', views.trainingPlan, name="training_plan"),
    
    path('sca/create_workplan', views.createWorkplan, name='create_workplan'),
    
    path('sca/update_user', views.update_user, name="update_user"),
    path('sca/update_attendance', views.updateAttendance, name="update_attendance"),
    
    path('sca/records_module', views.records_module, name="records_module"),
    path('sca/certificate_review', views.certificate_review, name="certificate_review"),
    
    path('sca/set_attendance', views.setAttendance, name="set_attendance"),
    path('sca/upload_file', views.uploadFile, name="upload_file"),
]