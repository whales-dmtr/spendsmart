from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from .forms import LoginForm, RegisterForm
from .models import Users


def is_valid(username, password):
    is_valid_username = Users.objects.filter(name=username).exists()
    if is_valid_username:
        checked_user = Users.objects.get(name=username)
        true_password = checked_user.password
        is_valid_password = check_password(password, true_password)
        if is_valid_password:
            return True 
        else:
            return False
    else:
        return False


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if is_valid(username, password):
            return render(request, 'users/profile.html', {'username': username})
        else: 
            login_form = LoginForm() 
            return render(request, 'users/login.html', {'message': 'You entered incorrect data', 'login_form': login_form})
    elif request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'users/login.html', {'login_form': login_form})


def view_register(request):
    register_form = RegisterForm() 
    return render(request, 'users/register.html', {'register_form': register_form})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = Users(
            name=username,
            password=make_password(password),
            email=email
        )
        user.save()

    return redirect('main')


def view_profile(request):
    if request.session['logged_in'] == True:
        return render(request, 'users/profile.html')
    elif request.session['logged_in'] == False:
        login_form = LoginForm() 
        return render(request, 'users/login.html', {'message': 'You\'re not logged into your account', 'login_form': login_form})
        

















