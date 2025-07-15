from django.contrib import admin


from .models import StudentProfile, TeacherProfile, SchoolProfile,Worksheet,Assignment,Notification
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(SchoolProfile)
admin.site.register(Worksheet)
admin.site.register(Assignment)
admin.site.register(Notification)
# Register your models here.
