from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from intervention.models import Mentor,Student,Admin,Appointment,Report
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        role = request.POST["role"]

        if role == "1":  # Student login
            try:
                student = Student.objects.get(studentId=username, studentPass=password)
                studentData = {
                    'student': student,
                    "message": "successfully"
                }
                # Redirect to student page upon successful login
                return redirect('student',studentId=student.studentId)
            except Student.DoesNotExist:
                # Handle invalid student ID or password
                message = {"message": "Invalid student ID or password"}
                return render(request, 'login.html', message)
        elif role == "2":  # Lecturer login
            try:
                lecturer = Mentor.objects.get(mentorId=username, mentorPass=password)
                lectData = {
                    'mentor': lecturer,
                    "message": "successfully"
                }
                # Redirect to lecturer page upon successful login
                return redirect('mentormainpage', MentorId=lecturer.mentorId)
            except Mentor.DoesNotExist:
                # Handle invalid lecturer ID or password
                lectData = {"message": "Invalid Lecturer ID or password"}
                return render(request, 'login.html', lectData)

        elif role == "3":  # Admin login
            try:
                admin = Admin.objects.get(adminId=username, adminPass=password)
                adminData = {
                    'admin': admin,
                    "message": "successfully"
                }
                # Redirect to admin page upon successful login
                return redirect('admin', adminId=admin.adminId)
            except Admin.DoesNotExist:
                # Handle invalid admin ID or password
                adminData = {"message": "Invalid Admin ID or password"}
                return render(request, 'login.html', adminData)

        else:
            # Handle invalid role
            message = {"message": "Invalid role"}
            return render(request, 'login.html', message)
    else:
        return render(request, 'login.html')
    

def student_view(request, studentId):
    try:
        student = Student.objects.filter(studentId=studentId).values()
        selectedStudent = Student.objects.get(studentId = studentId)
        mentor = Mentor.objects.all().values()
        app = Report.objects.filter(studentId=selectedStudent.studentId).values
        student_details = {
            'studentDetails': student,
            # 'details': details,
            'mentorDetails':mentor,
            'selectedStudent':selectedStudent,
            'Allreport':app
            
        }

        return render(request, 'studentPage.html', student_details)
    except Student.DoesNotExist:
        # Handle case where student with specified ID doesn't exist
        return HttpResponse("Student not found")
    
def mentor_view(request, MentorId):
    mentorDetails = Mentor.objects.get(mentorId=MentorId) 
    studentDetails = Student.objects.all().values()
    obj ={
        "mode":"students",
        "studentDetails": studentDetails,
        "mentorDetails": mentorDetails,
    }

    return render(request, 'mentorPage.html', obj)

def mentor_view_mentee(request, MentorId): 
    mentorDetails = Mentor.objects.get(mentorId=MentorId) 
    studentDetails = Student.objects.filter(mentorId = mentorDetails.mentorId)
    obj ={
        "mode":"mentee",
        "studentDetails": studentDetails,
        "mentorDetails": mentorDetails,

    }

    return render(request, 'mentorPage.html', obj)

def student_view_report(request,studentId):

    student = Student.objects.get(studentId=studentId)
    context = {
        'selectedStudent':student
    }
    return render(request, 'reportPage.html',context)

def student_post_report(request,studentId):

    student = Student.objects.get(studentId=studentId)
    context = {
        'selectedStudent':student
    }
    return render(request, 'reportPage.html',context )

def submitReport(request, studentId):
    if request.method == "POST":
        student_id = request.POST["studentId"]
        report_id = request.POST['reportID']
        mentor_id = request.POST["mentorid"]
        Date = request.POST["Date"]
        report_type = request.POST["reportType"]
        report = request.POST["studentReport"]
        
        stuid = Student.objects.get(studentId=student_id)
        mentor = Mentor.objects.get(mentorId=mentor_id)
        
        addToReport = Report(reportId=report_id, reportType=report_type ,  reportProg=report, date=Date, studentId=stuid, mentorId=mentor )
        addToReport.save()
    return redirect('student',studentId=studentId)

def mentorDisplay(request, MentorId):
    report = Report.objects.all().values()
    mentor = Mentor.objects.get(mentorId=MentorId)
    context = {
        "Allreport":report,
        'mentorDetails':mentor
    }
    return render(request,"mentorHomePage.html",context)

def studentDisplay(request, studentId):
    report = Report.objects.all().values()
    student = Mentor.objects.get(studentId=studentId)
    context = {
        "Allreport":report,
        'selectedStudents':student
    }
    return render(request,"studentPage.html",context)

def makeAppointment(request, MentorId, studentId):
    allMentor = Mentor.objects.all().values()
    mentor = Mentor.objects.get(mentorId=MentorId)
    student = Student.objects.get(studentId=studentId)
    context = {
        "AllAppoitment":allMentor,
        'mentorDetails':mentor,
        'selectedStudent':student
    }
    return render(request,'appoinmentMentor.html',context)

def submitAppointment(request, MentorId):
    if request.method == "POST":
        student_id = request.POST["studentId"]
        mentor_id = request.POST["mentorid"]
        Date = request.POST["Date"]
        Time = request.POST["Time"]
        desc = request.POST["description"]
        Venue = request.POST["venue"]
        
        stuid = Student.objects.get(studentId=student_id)
        mentor = Mentor.objects.get(mentorId=mentor_id)
        
        addToApp = Appointment(Report=desc , date=Date, time=Time, studentId=stuid, mentorId=mentor, venue=Venue )
        addToApp.save()
    return redirect('mentormainpage', MentorId=MentorId)

def admin_view(request,adminId):
    admin = Admin.objects.get(adminId=adminId)
    student = Student.objects.all().values()
    context ={
        "adminDetails" : admin,
        "studentDetails": student
    }

    return render(request,'adminPage.html',context)

def adminStudent_view(request,adminId): 
    studentDetails = Student.objects.all().values() 
    admin = Admin.objects.get(adminId=adminId)

    obj ={
        "studentDetails": studentDetails,
        "adminDetails":admin,
    }

    return render(request, 'studentAdminPage.html', obj)

def addStudent(request,adminId):
    add = Student.objects.all().values()
    admin = Admin.objects.get(adminId=adminId)
    mentor = Mentor.objects.all().values()
    obj = {
        "addStudent":add,
        'adminDetails':admin,
        'allMentor':mentor
    }
    return render(request, 'adminAddStudent.html',obj)

# 
def submitAddStudent(request,adminId):
    if request.method == "POST":
        studId = request.POST["studentid"]
        studname = request.POST["studentname"]
        menId = request.POST["mentorId"]
        studpass = request.POST["studentPassword"]
        studAddress = request.POST["studentAddress"]
        studNo = request.POST["studentno"]

        # stuid = Student.objects.get(studentId=studId)
        mentor = Mentor.objects.get(mentorId=menId)

        addtoAdmin = Student(studentId=studId,studentName=studname,mentorId=mentor,studentPass=studpass,StudentAddress=studAddress,studentNo=studNo)
        addtoAdmin.save()
    return redirect('admin',adminId = adminId)

def adminMentor_view(request,adminId): 
    mentor = Mentor.objects.all().values() 
    admin = Admin.objects.get(adminId=adminId)

    obj ={
        "mentorDetails": mentor,
        "adminDetails":admin
    }

    return render(request, 'MentorAdminPage.html', obj)

def addMentor(request,adminId):
    add = Mentor.objects.all().values()
    admin = Admin.objects.get(adminId=adminId)
    obj = {
        "addMentor":add,
        'adminDetails':admin
    }
    return render(request, 'adminaddMentor.html',obj)

def submitAddmentor(request,adminId):
    if request.method == "POST":
        menId = request.POST["mentorid"]
        menname = request.POST["mentorname"]
        menpass = request.POST["menPass"]
        menSub = request.POST["mentorsubject"]
        menNo = request.POST["menNo"]

        # stuid = Student.objects.get(studentId=studId)
        # mentor = Mentor.objects.get(mentorId=menId)

        addtoAdmin = Mentor(MentorName=menname,mentorId=menId,mentorPass=menpass,mentorSubject=menSub,mentorNo= menNo)
        addtoAdmin.save()
    return redirect('Mentoradmin',adminId = adminId)

def searchMentor(request,adminId):

    findmentor=Mentor.objects.filter(Q(mentorId=request.GET.get('search')))
    adminDetails=Admin.objects.get(adminId=adminId)
    dict = {
        'mentorDetails' : findmentor,
        'adminDetails':adminDetails
    }
    return render(request, 'MentorAdminPage.html', dict)

def searchStudent(request,adminId):

    findstudent=Student.objects.filter(Q(studentId=request.GET.get('studentId')))
    adminDetails=Admin.objects.get(adminId=adminId)
    dict = {
        'studentDetails' : findstudent,
        'adminDetails':adminDetails
    }
    return render(request, 'StudentAdminPage.html', dict)

def adminDeleteStudent(request,adminId,studID):
    selected_student = Student.objects.get(studentId=studID)

    selected_student.delete()

    return redirect('Studentadmin',adminId=adminId)

def adminUpdateStudent(request,adminId,studID):

    if request.method=="POST":
        studentId = request.POST["studentid"]
        studentAddress = request.POST["studentAddress"]
        studentNo = request.POST["studentno"]
        studentcour = request.POST["studentcourse"]

        selected_student=Student.objects.get(studentId = studentId)

        selected_student.studentNo=studentNo
        selected_student.StudentAddress=studentAddress
        selected_student.Studentcourse=studentcour

        selected_student.save()

        return redirect("Studentadmin",adminId=adminId)

    update = Student.objects.all().values()
    admin = Admin.objects.get(adminId=adminId)
    student = Student.objects.get(studentId=studID)
    obj = {
        "updateStudent":update,
        'adminDetails':admin,
        "studentDetails":student
    }
    return render(request, 'updateAdminStudent.html',obj)

def adminDeleteMentor(request,adminId,mentorID):
    selected_mentor = Mentor.objects.get(mentorId=mentorID)

    selected_mentor.delete()

    return redirect('Mentoradmin',adminId=adminId)

def adminUpdateMentor(request,adminId,mentorID):

    if request.method=="POST":
        mentorId = request.POST["mentorid"]
        mentorSub = request.POST["mentorsubject"]
        mentorno = request.POST["mentorNo"]

        selected_mentor=Mentor.objects.get(mentorId = mentorID)

        selected_mentor.mentorNo=mentorno
        selected_mentor.mentorSubject=mentorSub
        selected_mentor.save()

        return redirect("Mentoradmin",adminId=adminId)

    update = Mentor.objects.all().values()
    admin = Admin.objects.get(adminId=adminId)
    mentor = Mentor.objects.get(mentorId=mentorID)
    obj = {
        "updateMentor":update,
        'adminDetails':admin,
        "mentorDetails":mentor
    }
    return render(request, 'UpdateAdminMentor.html',obj)
    