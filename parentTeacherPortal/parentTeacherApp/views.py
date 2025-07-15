from datetime import datetime
import os
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import json
import json
from .utility import notifications
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.template.defaultfilters import lower
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt

from .models import TeacherProfile, StudentProfile, SchoolProfile, Worksheet, Assignment, Notification


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.username.split("_", 1)[1] == 'teacher':
        if request.user.TeacherProfile.teacher_school is None:
            school_profile_list = SchoolProfile.objects.all()
            for i in school_profile_list:
                if request.user in i.teacher_requests.all():
                    request.school_request = i
        assignments = Assignment.objects.filter(assigned_by=request.user)
        request.assignments = assignments
        request.notifications = Notification.objects.filter(user=request.user)
        return render(request, 'teacher_profile.html')
    elif request.user.username.split("_", 1)[1] == 'school':
        request.worksheet = Worksheet.objects.all()
        return render(request, 'school_profile.html')
    elif request.user.username.split("_", 1)[1] == 'student':
        request.notifications = Notification.objects.filter(user=request.user)
        return render(request, 'student_profile.html')
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
            notifications(user=user, user2=schoolprofile.user, Type="AYR")
        elif user.username.split("_", 1)[1] == 'student':
            schoolprofile.student_requests.remove(user)
            schoolprofile.students.add(user)
            user.StudentProfile.student_school = schoolprofile
            user.StudentProfile.save()
            notifications(user=user, user2=schoolprofile.user, Type="AYR")
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
    if (request.POST.get("map") != None):
        class_subject_map = json.loads(request.POST.get("map"))
        for pair in class_subject_map:
            standard = pair.split(':')[0]
            edit_user.TeacherProfile.class_subject_map[standard].remove(pair.split(':')[1])
            if len(edit_user.TeacherProfile.class_subject_map[standard]) == 0:
                edit_user.TeacherProfile.class_subject_map.pop(standard)
            edit_user.TeacherProfile.save()
    # else:

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
        standard = request.POST.get("standard")
        if standard in teacher_profile.class_subject_map:
            (teacher_profile.class_subject_map[standard]).append(request.POST.get("subject"))
            teacher_profile.save()
        else:
            map = {request.POST.get("standard"): [request.POST.get("subject")]}
            teacher_profile.class_subject_map.update(map)
            teacher_profile.save()
        notifications(user=teacher_profile.user, user2=request.user, Type="YHBA", standard=standard,
                      subject=request.POST.get("subject"))
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


def display_words(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'static', 'data.json')
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        standard = str(data.get("standard", ""))
        subjects = data.get("subjects", {})
        for subject, books in subjects.items():
            for book_name, book_data in books.items():
                for chapter_name, chapter_data in book_data.items():
                    for worksheet in chapter_data:
                        worksheetObject = Worksheet.objects.create(standard=standard, subject=subject,
                                                                   chapter=chapter_name, worksheet_name=worksheet)
                        print(worksheet)
                        worksheetObject.save()
    return HttpResponse("Done")


@csrf_exempt
def add_workbook(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        schoolprofile = request.user.SchoolProfile
        worksheet = Worksheet.objects.get(worksheet_id=request.POST.get('workbook_id'))
        schoolprofile.school_workbooks.add(worksheet)
        schoolprofile.save()
    return HttpResponse("Done")


@csrf_exempt
def remove_workbook(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        schoolprofile = request.user.SchoolProfile
        worksheet = Worksheet.objects.get(worksheet_id=request.POST.get('workbook_id'))
        schoolprofile.school_workbooks.remove(worksheet)
        schoolprofile.save()
    return HttpResponse("Done")


@csrf_exempt
def get_teacher_standard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        return HttpResponse(
            json.dumps((TeacherProfile.objects.get(teacher_id=request.POST.get("user_id"))).class_subject_map))


@csrf_exempt
def get_worksheet(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        worksheets = []
        if request.user.username.split("_", 1)[1] == 'school':
            teacherprofile = TeacherProfile.objects.get(teacher_id=request.POST.get("user_id"))
            for subject in teacherprofile.class_subject_map[request.POST.get("standard")]:
                for worksheet in request.user.SchoolProfile.school_workbooks.all():
                    if worksheet not in teacherprofile.teacher_workbooks.all():
                        if worksheet.standard == request.POST.get("standard"):
                            if worksheet.subject == lower(subject):
                                worksheets.append(
                                    {"worksheet_name": worksheet.worksheet_name, "standard": worksheet.standard,
                                     "subject": worksheet.subject,
                                     "chapter": worksheet.chapter, "worksheet_id": worksheet.worksheet_id})
        if request.user.username.split("_", 1)[1] == 'teacher':
            for worksheet in request.user.TeacherProfile.teacher_workbooks.all():
                print(lower(request.POST.get("subject")))
                if worksheet.subject == lower(request.POST.get("subject")):
                    worksheets.append(
                        {"worksheet_name": worksheet.worksheet_name, "standard": worksheet.standard,
                         "subject": worksheet.subject,
                         "chapter": worksheet.chapter, "worksheet_id": worksheet.worksheet_id})
        worksheets = json.dumps(worksheets)
        return HttpResponse(worksheets)


@csrf_exempt
def assign_worksheet(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        if request.user.username.split("_", 1)[1] == 'school':
            teacherprofile = TeacherProfile.objects.get(teacher_id=request.POST.get("teacher_id"))
            teacherprofile.teacher_workbooks.add(Worksheet.objects.get(worksheet_id=request.POST.get("worksheet_id")))
            teacherprofile.save()
            notifications(user=teacherprofile.user, user2=request.user, Type="ANWATY",
                          worksheet=Worksheet.objects.get(worksheet_id=request.POST.get("worksheet_id")))
        if request.user.username.split("_", 1)[1] == 'teacher':
            worksheet = Worksheet.objects.get(worksheet_id=request.POST.get("worksheet_id"))
            assignment = Assignment.objects.create(standard=worksheet.standard, subject=worksheet.subject,
                                                   assigned_by=request.user, due_date=request.POST.get('duedate'))
            assignment.worksheet.add(worksheet)
            assignment.save()
            students = StudentProfile.objects.filter(standard=worksheet.standard)
            for student in students:
                assignment.assigned_student.add(student.user)
                student.student_assignment_list.add(assignment)
                student.save()
                assignment.save()
                notifications(user=student.user, user2=request.user, Type="ANAATY", assignment=assignment)
    return HttpResponse("done")


@csrf_exempt
def mark_as_done(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        assignment = Assignment.objects.get(assignment_id=request.POST.get("assignment_id"))
        assignment.submit_status.add(request.user)
        assignment.save()
        notifications(user=assignment.assigned_by, Type="FCSAC", user2=request.user, assignment=assignment)
    return HttpResponse("done")


@csrf_exempt
def notification_seen(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        for notification in Notification.objects.filter(user=request.user).exclude(status=True):
            notification.status = True
    return HttpResponse("done")
