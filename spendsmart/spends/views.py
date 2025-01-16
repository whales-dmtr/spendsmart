from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Spends, Categories, Users
from .forms import AddSpendForm, CreateCategoryForm

def view_all_spends(request):
   if 'user_id' in request.session:
        user = Users.objects.get(id=request.session['user_id'])
    
        return render(request, 'spends/index.html', {'all_spends': Spends.objects.all()})
   else:
       return redirect('login')


def add_spend(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        desc = request.POST['description']
        amount = request.POST['amount']
        category = request.POST['category']
        new_spend = Spends(
            user_id=user_id,
            desc=desc,
            amount=amount,
            category_id=category
        ) 
        new_spend.save()
    elif request.method == 'GET':
        if 'user_id' in request.session:
            view_form = AddSpendForm()
            return render(request, 'spends/add_spends.html', {'view_form': view_form})
        else:
            redirect('login')


def create_category(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        name_of_category = request.POST['name']
        category = Categories(user_id=user_id, name=name_of_category)
        category.save()
        return redirect('main')
    elif request.method == 'GET':
        if 'user_id' in request.session:
            view_form = CreateCategoryForm()
            return render(request, 'spends/create_category.html', {'view_form': view_form})
        else:
            redirect('login')


def control_panel(request):
    if request.method == 'POST':
        if request.POST['type'] == 'profile':
            return redirect('profile')
        elif request.POST['type'] == 'shows_categories_form':
            pass
        elif request.POST['type'] == 'create_category':
            return redirect('create_category')
        elif request.POST['type'] == 'sort_by_categories_form':
            pass
        elif request.POST['type'] == 'add_spend':
            return redirect('add_spend')


 
