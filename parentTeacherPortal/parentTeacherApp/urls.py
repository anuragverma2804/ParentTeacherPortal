from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout_user', views.logout_user, name='logout'),
    path('accept_request', views.accept_requests, name='accept_requests'),
    path('remove_requests', views.remove_requests, name='remove_requests'),
    path('remove_teacher', views.remove_teacher, name='remove_teacher'),
    path('send_request', views.send_request, name='send_request'),
    path('edit_school/<int:id>', views.edit_school, name='edit_school'),
    path('edit_student/<int:id>', views.edit_student, name='edit_student'),
    path('edit_teacher/<int:id>', views.edit_teacher, name='edit_teacher'),
    path('add_workbooks', views.add_workbooks, name='add_workbooks'),
    path('assign_workbook', views.assign_workbook, name='assign_workbook'),
    path('assign_class_subject', views.assign_class_subject, name='assign_class_subject'),
    path('get_class_subject_list', views.get_class_subject_list, name='get_class_subject_list'),
    path('school_list', views.school_list, name='school_list'),
]