from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Teacher_profile, Parent_profile
# Create your views here.

def home(request):
    return render(request, 'index.html')


def login_user(request):
    if request.method == 'POST':
        role=request.POST.get('role')
        email = request.POST.get('email')
        passw = request.POST.get('pass')
        username = email.split('@')[0]
        user = authenticate(username=username, password=passw)
        profile=None
        if user is not None:
            if (role == "teacher"):
                try:
                    profile=Teacher_profile.objects.get(email=email)
                except ObjectDoesNotExist:
                    messages.error(request, "Incorrect Role")
                if profile is not None:
                    login(request, user)
                    return render(request, 'teacher_profile.html')
            elif (role == "parent"):
                try:
                    profile=Parent_profile.objects.get(email=email)
                except ObjectDoesNotExist:
                    print(user)
                    messages.error(request, "Incorrect Role")
                if profile is not None:
                    login(request, user)
                    return render(request, 'parent_profile.html')
        else:
            messages.error(request, "Incorrect Credentials")
            return redirect('login')
    return render(request, 'login.html')



def signup(request):
    if request.method == 'POST':
        role=request.POST.get('role')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        number=request.POST.get('number')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        username=email.split('@')[0]
        if pass1==pass2:
            myuser = User.objects.create_user(username=username, email=email, password=pass1)
            myuser.save()
            if role=='teacher':
                profile = Teacher_profile(user=User.objects.get(username=username),
                                   first_name=fname, last_name=lname, phone=number,email=email)
                profile.save()
                return render(request, 'login.html')

            elif role=='parent':
                profile = Parent_profile(user=User.objects.get(username=username),
                                   first_name=fname, last_name=lname, phone=number,email=email)
                profile.save()
                return render(request, 'login.html')
            else:
                return render(request, 'signup.html')
    return render(request, 'signup.html')
