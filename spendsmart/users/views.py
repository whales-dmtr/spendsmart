from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from .forms import LoginForm, RegisterForm, EditFieldForm
from .models import Users, Profile


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
            request.session['user_id'] = Users.objects.get(name=username).id
            return redirect('profile')
        else: 
            login_form = LoginForm() 
            return render(request, 'users/login.html', {'login_form': login_form, 
                                                        'message': 'You entered incorrect username or password :('})
    elif request.method == 'GET':
        login_form = LoginForm() 
        return render(request, 'users/login.html', 
                      context={'login_form': login_form})


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

        return redirect('main')
    elif request.method == 'GET':
        register_form = RegisterForm() 
        return render(request, 'users/register.html', {'register_form': register_form})


def get_profile_data(request):
    user = Users.objects.get(id=request.session['user_id'])
    profile = Profile.objects.get(user_id=user.id)

    fields_data = [
        ['Username', user.name, 'name'],  # label, data info, key for edit
        ['Password', user.password, 'password'],
        ['First name', profile.first_name, 'first_name'],
        ['Last name', profile.last_name, 'last_name'],
        ['Birthday', profile.birthday_date, 'birthday'],
        ['About you', profile.desc, 'desc'],
    ]

    idx = 0
    for label, data, key_edit in fields_data:
        if data is None:
            fields_data[idx][1] = '-'
        elif key_edit == 'password':
            fields_data[idx][1] = '********'
        idx += 1

    context = {
        'fields_data': fields_data, 
        'welcome_name': profile.first_name if profile.first_name is not None else user.name,
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
        edit_form = EditFieldForm()
        profile_data = get_profile_data(request)
        edited_field = request.POST['edit_field']
        return render(request, 'users/profile.html', context={'edit_form': edit_form, **profile_data, 'edited_field': edited_field})
    

def edit_profile(request):
    if request.method == 'POST':
        if request.POST['name'] == 'name':
            user = Users.objects.get(id=request.session['user_id'])
            setattr(user, request.POST['name'], request.POST['field'])
            user.save()
        elif request.POST['name'] == 'password':
            user = Users.objects.get(id=request.session['user_id'])
            setattr(user, request.POST['name'], make_password(request.POST['field']))
        else:
            profile = Profile.objects.get(user_id=request.session['user_id'])
            setattr(profile, request.POST['name'], request.POST['field'])
            profile.save()
            
        return redirect('profile')


def logout(request):
    del request.session['user_id']
    return redirect('main')













