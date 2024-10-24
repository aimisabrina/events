from django.contrib import admin
from .models import Program, Student,Staff,Event,Attendance
admin.site.register(Student)
admin.site.register(Program)
admin.site.register(Staff)
admin.site.register(Event)
admin.site.register(Attendance)
# Register your models here.
