from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    standard = models.CharField(max_length=2, blank=False)
    guardian_name = models.CharField(max_length=50, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    student_workbook_list = models.TextField(validators=[validate_comma_separated_integer_list], null=True)
    student_school = models.ForeignKey('SchoolProfile', related_name='Student_School', default=None, blank=True,
                                       on_delete=models.CASCADE)

    objects = models.Manager()


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    classes_list = models.TextField(validators=[validate_comma_separated_integer_list])
    teacher_workbook_list = models.TextField(validators=[validate_comma_separated_integer_list], null=True)
    teacher_school = models.ForeignKey('SchoolProfile', related_name='Teacher_School', default=None, blank=True,
                                       on_delete=models.CASCADE)

    objects = models.Manager()


class SchoolProfile(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50, primary_key=True, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    city = models.CharField(max_length=50, blank=False, default=None)
    state = models.CharField(max_length=50, blank=False, default=None)
    pincode = models.CharField(max_length=10, blank=False, default=None)
    school_workbook_list = models.TextField(validators=[validate_comma_separated_integer_list], null=True)

    objects = models.Manager()
