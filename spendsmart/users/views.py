from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from .forms import (EmailEditForm, LoginForm, RegisterForm, EditFieldForm, PasswordEditForm, 
                    BirthdayEditForm, DescEditForm)
from .models import Users, Profile
import ast


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


def is_valid_endpoint(request):
    if request.method == 'GET':
        # take parameters from the HTTP request body
        # and convert their to dict
        body = ast.literal_eval(str(request.body)[2:-1])  
        return JsonResponse(body)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if is_valid(username, password):
            request.session['user_id'] = Users.objects.get(name=username).id
            return redirect('main')
        else: 
            login_form = LoginForm() 
            return render(
                request=request, 
                template_name='users/login.html', 
                context={
                    'login_form': login_form,                       
                    'message': 'You entered incorrect username or password :('
                }
            )
        
    elif request.method == 'GET':
        login_form = LoginForm() 
        return render(
            request=request, 
            template_name='users/login.html',         
            context={
                'login_form': login_form                  
            }
        )


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
        
        profile = Profile(user_id=user.id)
        profile.save()

        request.session['user_id'] = Users.objects.get(name=username).id
        return redirect('main')
    elif request.method == 'GET':
        register_form = RegisterForm() 
        return render(
            request=request, 
            template_name='users/register.html', 
            context={
                'register_form': register_form
            }
        )


def get_profile_data(request):
    user = Users.objects.get(id=request.session['user_id'])
    profile = Profile.objects.get(user_id=user.id)

    fields_data = [
        # label, data, key for edit, max length
        ['Username', user.name, 'name', 15],  
        ['Password', user.password, 'password', 20],
        ['Email', user.email, 'email', 254],
        ['First name', profile.first_name, 'first_name', 25],
        ['Last name', profile.last_name, 'last_name', 30],
        ['Birthday', profile.birthday_date, 'birthday', None],
        ['About you', profile.desc, 'desc', 200],
    ]

    idx = 0
    for label, data, key_edit, max_len in fields_data:
        if data is None:
            fields_data[idx][1] = '-'
        elif key_edit == 'password':
            fields_data[idx][1] = '********'
        idx += 1

    context = {
        'fields_data': fields_data, 
        'welcome_name': (profile.first_name if profile.first_name != ''
                         else user.name),
    }

    return context


def profile(request):
    if request.method == 'GET':
        if 'user_id' in request.session:
            profile_data = get_profile_data(request)
            return render(request, 'users/profile.html', context=profile_data)
        else:
            return redirect('login')
    elif request.method == 'POST':
        profile_data = get_profile_data(request)
        edited_field = request.POST['edit_field']

        if edited_field == 'password':
            edit_form = PasswordEditForm()
        elif edited_field == 'email':
            edit_form = EmailEditForm()
        elif edited_field == 'birthday':
            edit_form = BirthdayEditForm()
        elif edited_field == 'desc':
            edit_form = DescEditForm(profile_data['fields_data'][-1][1])
        else:
            # Choose specific length and hint
            for label, form, idx, max_len in profile_data['fields_data']:
                if idx == edited_field:
                    edit_form = EditFieldForm(max_len=max_len, hint=label)

        return render(
            request=request, 
            template_name='users/profile.html', 
            context={
                'edit_form': edit_form, 
                **profile_data, 
                'edited_field': edited_field
            }
        )
    

def edit_profile(request):
    if request.method == 'POST':
        if request.POST['type'] == 'save':
            if request.POST['name'] == 'name':
                user = Users.objects.get(id=request.session['user_id'])
                setattr(user, request.POST['name'], request.POST['field'])
                user.save()
            elif request.POST['name'] == 'password':
                user = Users.objects.get(id=request.session['user_id'])
                setattr(
                    user, request.POST['name'], 
                    make_password(request.POST['field'])
                )
            elif request.POST['name'] == 'birthday':
                profile = Profile.objects.get(user_id=request.session['user_id'])
                birthday_date = f'{request.POST['field_year']}-{request.POST['field_month']}-{request.POST['field_day']}'
                setattr(profile, f"{request.POST['name']}_date", birthday_date)
                profile.save()
            else:
                profile = Profile.objects.get(user_id=request.session['user_id'])
                setattr(profile, request.POST['name'], request.POST['field'])
                profile.save()
                
            return redirect('profile')
        elif request.POST['type'] == 'esc':
            return redirect('profile')
    else:
        return redirect('login')


def logout(request):
    if request.method == 'POST':
        if request.POST['type'] == 'logout':
            del request.session['user_id']
            return redirect('main')
        elif request.POST['type'] == 'homepage':
            return redirect('main')
    else:
        return redirect('login')

        













