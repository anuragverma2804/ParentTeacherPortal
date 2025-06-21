from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import json
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from .models import TeacherProfile, StudentProfile, SchoolProfile


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.username.split("_", 1)[1] == 'teacher':
        if request.user.TeacherProfile.teacher_school is None:
            school_profile_list = SchoolProfile.objects.all()
            for i in school_profile_list:
                if request.user in i.teacher_requests.all():
                    request.school_request = i
        return render(request, 'teacher_profile.html')
    elif request.user.username.split("_", 1)[1] == 'school':
        return render(request, 'school_profile.html')
    elif request.user.username.split("_", 1)[1] == 'student':
        return render(request, 'parent_profile.html')
    else:
        return redirect('login')


def login_user(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        email = request.POST.get('email')
        passw = request.POST.get('pass')
        username = email.split('@')[0]
        username = username + "_" + role
        user = authenticate(username=username, password=passw)
        profile = None
        if user is not None:
            if role == "teacher":
                try:
                    profile = TeacherProfile.objects.get(email=email)
                except ObjectDoesNotExist:
                    messages.error(request, "Incorrect Role")
                if profile is not None:
                    login(request, user)
                    return redirect('home')
            elif role == "student":
                try:
                    profile = StudentProfile.objects.get(email=email)
                except ObjectDoesNotExist:
                    messages.error(request, "Incorrect Role")
                if profile is not None:
                    login(request, user)
                    return redirect('home')
            elif role == "school":
                try:
                    profile = SchoolProfile.objects.get(email=email)
                except ObjectDoesNotExist:
                    messages.error(request, "Incorrect Role")
                if profile is not None:
                    login(request, user)
                    return redirect('home')
        else:
            messages.error(request, "Incorrect Credentials")
            return redirect('login')
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        email = request.POST.get('email')
        number = request.POST.get('number')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        username = email.split('@')[0]
        username = username + "_" + role

        if pass1 == pass2:
            myuser = User.objects.create_user(username=username, email=email, password=pass1)
            myuser.save()
            if role == 'teacher':
                first_name = request.POST.get('fname')
                last_name = request.POST.get('lname')
                school = SchoolProfile.objects.get(school_id=request.POST.get('teacher_school'))
                school.teacher_requests.add(myuser)
                profile = TeacherProfile(user=User.objects.get(username=username),
                                         first_name=first_name, last_name=last_name, phone=number, email=email)
                try:
                    file_name = str(request.FILES['passportphoto'])
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        profile.profileImg = request.FILES['passportphoto']
                    else:
                        return HttpResponseRedirect('signup')
                except Exception as e:
                    print(e)
                profile.save()
                return render(request, 'login.html')

            elif role == 'student':
                first_name = request.POST.get('fname')
                last_name = request.POST.get('lname')
                standard = request.POST.get('standard')
                guardian_name = request.POST.get('guardian_name')
                school = SchoolProfile.objects.get(school_id=request.POST.get('student_school'))
                school.student_requests.add(myuser)
                profile = StudentProfile(user=User.objects.get(username=username),
                                         first_name=first_name, last_name=last_name, phone=number, email=email,
                                         standard=standard, guardian_name=guardian_name)
                try:
                    file_name = str(request.FILES['passportphoto'])
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        profile.profileImg = request.FILES['passportphoto']
                    else:
                        return HttpResponseRedirect('signup')
                except Exception as e:
                    print(e)
                profile.save()
                return render(request, 'login.html')
            elif role == 'school':
                school_name = request.POST.get('school_name')
                city = request.POST.get('city')
                state = request.POST.get('state')
                pincode = request.POST.get('pin_code')
                profile = SchoolProfile(user=User.objects.get(username=username),
                                        name=school_name, phone=number, email=email, city=city, state=state,
                                        pincode=pincode)
                try:
                    file_name = str(request.FILES['passportphoto'])
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        profile.profileImg = request.FILES['passportphoto']
                    else:
                        return HttpResponseRedirect('signup')
                except Exception as e:
                    print('exception')
                    print(e)
                profile.save()
                return render(request, 'login.html')
            else:
                return render(request, 'signup.html')
    return render(request, 'signup.html')


def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('login')
    auth.logout(request)
    logout(request)
    request.session.flush()
    request.user = AnonymousUser
    return redirect('home')


@csrf_exempt
def accept_requests(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        id = request.POST.get('user_id')
        user = User.objects.get(id=id)
        schoolprofile = SchoolProfile.objects.get(user=request.user)
        if user.username.split("_", 1)[1] == 'teacher':
            schoolprofile.teacher_requests.remove(user)
            schoolprofile.teachers.add(user)
            user.TeacherProfile.teacher_school = schoolprofile
            user.TeacherProfile.save()
        elif user.username.split("_", 1)[1] == 'student':
            schoolprofile.student_requests.remove(user)
            schoolprofile.students.add(user)
    return HttpResponse(request.POST.get('user_id'))


@csrf_exempt
def remove_requests(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        id = request.POST.get('user_id')
        user = User.objects.get(id=id)
        schoolprofile = SchoolProfile.objects.get(user=request.user)
        if user.username.split("_", 1)[1] == 'teacher':
            schoolprofile.teacher_requests.remove(user)
        elif user.username.split("_", 1)[1] == 'student':
            schoolprofile.student_requests.remove(user)
    return HttpResponse(request.POST.get('user_id'))


@csrf_exempt
def remove_teacher(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        id = request.POST.get('user_id')
        user = User.objects.get(id=id)
        schoolprofile = SchoolProfile.objects.get(user=request.user)
        if user.username.split("_", 1)[1] == 'teacher':
            schoolprofile.teachers.remove(user)
            user.TeacherProfile.teacher_school = None
            user.TeacherProfile.save()
    return HttpResponse(request.POST.get('user_id'))


@csrf_exempt
def send_request(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        school_profile = SchoolProfile.objects.get(school_id=request.POST.get("school_id"))
        school_profile.teacher_requests.add(request.user)
    return HttpResponse(request.POST.get("school_id"))


def reset_password(request, id):
    pass


def edit_school(request, id):
    return render(request, 'edit_school.html')

@csrf_exempt
def edit_teacher(request, id):
    edit_user = User.objects.get(id=id)
    request.edit_user = edit_user
    print(json.loads(request.POST.get("map")))
    # for i,j in (json.loads(request.POST.get("map"))).items():
    #     print(i,j)
    return render(request, 'edit_teacher.html')


def edit_student(request, id):
    return render(request, 'edit_student.html')


def add_workbooks(request):
    pass


def assign_workbook(request):
    pass


@csrf_exempt
def school_list(request):
    data = []
    items = SchoolProfile.objects.all()
    for i in items:
        data.append({"name": i.name, "id": i.school_id})
    response = json.dumps(data, default=str)
    return HttpResponse(response)


@csrf_exempt
def assign_class_subject(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        teacher_profile = TeacherProfile.objects.get(teacher_id=request.POST.get("teacher"))
        map = {request.POST.get("standard"): request.POST.get("subject")}
        teacher_profile.class_subject_map.update(map)
        teacher_profile.save()
    return HttpResponse("response")


@csrf_exempt
def get_class_subject_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        teacher_profile = TeacherProfile.objects.get(teacher_id=request.POST.get("teacher_id"))
        standard = request.POST.get("standard")
        subject = []
        for key, value in teacher_profile.class_subject_map.items():
            if key == standard:
                subject.append(value)
        return HttpResponse(subject if len(subject) > 0 else None)
