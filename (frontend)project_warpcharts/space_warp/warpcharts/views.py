from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import request
import pandas as pd
import io
from .models import File
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.

def home_page(request):

    if request.method == 'POST':
        user_name = request.POST['username']
        user_pass  = request.POST['password']

        #Authenticate
        user = authenticate(request, username = user_name, password = user_pass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home_page')
        
        else:
            messages.error(request, "Error Occured Try Again")
            return redirect('login_page')
    
    else:
        return render(request, 'page_home/index.html', {})

def login_page(request):
    return render(request, 'page_login/index.html', {})


def logout_user(request):
    logout(request)
    messages.info(request, "Logged Out")
    return redirect('home_page')

def user_profile(request):
    return render(request, 'page_user_profile/index.html', {})

def signup(request):

    if request.method == 'POST':
        name = request.POST['name']
        user_name = request.POST['username']
        user_email = request.POST['email']
        user_pass = request.POST['password']


        #Creating User
        
        if User.objects.filter(username=user_name).exists():
            messages.error(request, 'username_error')
            return redirect('signup')
        
        elif User.objects.filter(email=user_email).exists():
            messages.info(request, 'email_error')
            return redirect('signup')
        
        else:
            user = User.objects.create_user(username=user_name, password=user_pass, email=user_email, first_name=name)
            user.save()
            login(request, user)
            messages.success(request, "Account Created!")
            return redirect('home_page')

    else:
        return render(request, 'page_sign_up/index.html', {})
    

def file_upload(request, type):

    if request.method == 'POST':

        File.objects.all().delete()
        print(File.objects.all())
        print(BASE_DIR)

        csv = request.FILES['file']
        File.objects.create(file = csv)

        file_name = request.FILES['file'].name
        request.session['file_name'] = file_name

        context = {
        'gtype':request.session["graph_type"],
        }
        return render(request, 'page_theme_options/index.html', context)

    else:
        request.session["graph_type"] = type
        request.session.modified = True

        context = {
            'gtype':request.session["graph_type"],
        }
        return render (request, 'page_upload/index.html', context)

def themes(request, type):
    return render (request, 'page_theme_options/index.html', {})