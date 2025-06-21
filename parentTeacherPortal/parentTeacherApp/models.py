from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list


class SchoolProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='SchoolProfile')
    school_id = models.AutoField(primary_key=True)
    teacher_requests = models.ManyToManyField(User, related_name='teacher_requests', default=None, blank=True)
    student_requests = models.ManyToManyField(User, related_name='student_requests', default=None, blank=True)
    teachers = models.ManyToManyField(User, related_name='teacher', default=None, blank=True)
    students = models.ManyToManyField(User, related_name='student', default=None, blank=True)
    name = models.CharField(max_length=50, blank=False)
    schoolImg = models.ImageField(upload_to='School/School Image', default='Images/default_page.png', null=False)
    email = models.EmailField(max_length=50, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    city = models.CharField(max_length=50, blank=False, default=None)
    state = models.CharField(max_length=50, blank=False, default=None)
    pincode = models.CharField(max_length=10, blank=False, default=None)
    school_workbook_list = models.TextField(validators=[validate_comma_separated_integer_list], null=True)

    objects = models.Manager()


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='StudentProfile')
    student_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    standard = models.CharField(max_length=5, blank=False)
    studentImg = models.ImageField(upload_to='Student/Student Image', default='Images/default_page.png', null=False)
    guardian_name = models.CharField(max_length=50, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    student_assignment_list = JSONField(default=dict)
    student_school = models.ForeignKey(SchoolProfile, related_name='Student_School', null=True, default=None,
                                       blank=True,
                                       on_delete=models.CASCADE)

    objects = models.Manager()


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='TeacherProfile')
    teacher_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    teacherImg = models.ImageField(upload_to='Teacher/Teacher Image', default='Images/default_page.png', null=False)
    phone = models.CharField(max_length=20, blank=False)
    class_subject_map = JSONField(default=dict)
    assigment_map = JSONField(default=dict)
    teacher_workbook_list = models.TextField(validators=[validate_comma_separated_integer_list], null=True)
    teacher_school = models.ForeignKey(SchoolProfile, related_name='Teacher_School', null=True, default=None,
                                       blank=True, on_delete=models.CASCADE)

    objects = models.Manager()
