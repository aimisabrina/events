from django.db import models

# Create your models here.
class Program(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    desc = models.TextField()

class Student(models.Model):
    studid = models.CharField(max_length=12,primary_key=True)
    studname = models.TextField()
    studpassword = models.CharField(max_length=10)
    studgender = models.CharField(max_length=8)
    studphone = models.CharField(max_length=20)
    code = models.ForeignKey(Program, on_delete = models.CASCADE)

class Staff(models.Model):
    fid = models.CharField(max_length=4, primary_key=True)
    fname = models.TextField()
    fpass = models.CharField(max_length=10)
    fposition = models.TextField()
    fphno = models.CharField(max_length=20)

class Event(models.Model):
    eventid = models.CharField(max_length=7, primary_key=True)
    eventname = models.TextField()
    eventdate = models.DateField()
    fid = models.ForeignKey(Staff, on_delete = models.CASCADE)
    eventvenue = models.TextField()
  
class Attendance(models.Model):
    attid = models.AutoField(max_length=7, primary_key=True)
    studentid = models.ForeignKey(Student, on_delete = models.CASCADE)
    eventid = models.ForeignKey(Event, on_delete = models.CASCADE)
    
