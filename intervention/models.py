from django.db import models

# Create your models here.

class Mentor (models.Model):
    mentorId = models.CharField(max_length=10, primary_key=True)
    MentorName = models.TextField(max_length=50)
    mentorPass = models.CharField(max_length=20)
    mentorSubject = models.TextField(max_length=30,blank=True,null=True)
    mentorNo =  models.TextField(max_length=30,blank=True,null=True)

class Student (models.Model):
    studentId = models.CharField(max_length=20, primary_key=True)
    studentName = models.TextField(max_length=20)
    mentorId = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    studentPass = models.CharField(max_length=20)    
    StudentAddress = models.TextField(blank=True,null=True)
    studentNo = models.TextField(max_length=20,blank=True,null=True)
    Studentcourse = models.TextField(max_length=30,blank=True,null=True)


class Admin (models.Model):
    adminId = models.CharField(max_length=20, primary_key=True)
    adminName = models.TextField(max_length=20)
    adminPass = models.CharField(max_length=20)

class Report(models.Model):
    reportId = models.CharField(max_length=20, primary_key=True)
    reportType = models.TextField(max_length=20)
    reportProg = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    studentId = models.ForeignKey(Student,on_delete=models.CASCADE)
    mentorId = models.ForeignKey(Mentor,on_delete=models.CASCADE)

class Appointment(models.Model):
    Report = models.TextField(blank=True, null=True)
    date = models.DateField(max_length=20)
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    mentorId = models.ForeignKey(Mentor,on_delete=models.CASCADE)
    studentId = models.ForeignKey(Student,on_delete=models.CASCADE)