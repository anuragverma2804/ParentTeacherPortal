from django.contrib import admin


from .models import StudentProfile, TeacherProfile, SchoolProfile
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(SchoolProfile)
# Register your models here.
