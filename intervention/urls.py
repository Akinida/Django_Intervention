from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('student/<str:studentId>', views.student_view, name='student'),
    path('student/<str:studentId>', views.studentDisplay,name='studentmainpage'),
    
    path('student/report/<str:studentId>', views.student_view_report, name='report'),
    path('student/report/submit/<str:studentId>', views.submitReport, name='submitReport'),
    path('student/report/post/<str:studentId>', views.student_post_report, name='studentReport'),

    path('mentor/<str:MentorId>', views.mentorDisplay,name='mentormainpage'),
    path('mentor/myStudent/<str:MentorId>', views.mentor_view,name='mentor'),
    path('mentor/myMentee/<str:MentorId>', views.mentor_view_mentee,name='mentee'),
    path('mentor/myAppointment/<str:MentorId>/<str:studentId>', views.makeAppointment,name='appointment'),
    path('mentor/report/submit/<str:MentorId>', views.submitAppointment, name='submitAppointment'),
    path('admin/<str:adminId>', views.admin_view, name='admin'),
    path('admin/<str:adminId>/studentDetails', views.adminStudent_view, name='Studentadmin'),

    # admin nak delete stuedent data
    path('admin/<str:adminId>/studentDetails/delete/<str:studID>', views.adminDeleteStudent, name='adminDeletestudent'),
    path('admin/<str:adminId>/studentDetails/update/<str:studID>', views.adminUpdateStudent, name='adminupdatestudent'),

    #admin nak delete data mentor
    path('admin/<str:adminId>/mentorDetails/delete/<str:mentorID>', views.adminDeleteMentor, name='adminDeletementor'),
    path('admin/<str:adminId>/mentorDetails/update/<str:mentorID>', views.adminUpdateMentor, name='adminUpdatementor'),


    # path('admin/<str:adminId>/studentDetails/delete/<str:studID>', views.adminDeleteStudent, name='adminDeleteStudent'),
    # admin nak add stuedent data
    path('admin/<str:adminId>/studentDetails/add', views.addStudent, name='addStudent'),
    path('admin/<str:adminId>/studentDetails/add/submit', views.submitAddStudent, name='submitAddStudent'),
    path('admin/<str:adminId>/mentorDetails', views.adminMentor_view, name='Mentoradmin'),
    path('admin/<str:adminId>/mentorDetails/add', views.addMentor, name='addmentor'),
    path('admin/<str:adminId>/mentorDetails/add/submit', views.submitAddmentor, name='submitAddMentor'),
    path("admin/<str:adminId>/searchmentor", views.searchMentor, name='searchMentor'),
    path("admin/<str:adminId>/searchstudent", views.searchStudent, name='searchStudent')


    
    
]