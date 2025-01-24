from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Spends, Categories, Users
from .forms import AddSpendForm, CreateCategoryForm, EditCategoryForm, EditSpendForm

def view_all_spends(request):
   if 'user_id' in request.session:
        user_id = Users.objects.get(id=request.session['user_id'])
        spends = Spends.objects.filter(user_id=user_id).order_by('-date')
        return render(request, 'spends/index.html', {
            'view_spends': spends.exists(),
            'all_spends': spends
        })
   else:
       return redirect('login')


def add_spend(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        desc = request.POST['description']
        amount = request.POST['amount']
        category = request.POST['category']

        date = f'{request.POST['date_year']}-{request.POST['date_month']}-{request.POST['date_day']}'

        new_spend = Spends(
            user_id=user_id,
            desc=desc,
            amount=amount,
            category_id=category,
            date=date,
        ) 
        new_spend.save()

        category = Categories.objects.get(id=request.POST['category'])
        category.update_category_amount()

        return redirect('main')
    elif request.method == 'GET':
        if 'user_id' in request.session:
            view_form = AddSpendForm(request.session['user_id'])
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
        elif request.POST['type'] == 'show_categories':
            return redirect('all_categories')
        elif request.POST['type'] == 'create_category':
            return redirect('create_category')
        elif request.POST['type'] == 'sort_by_categories_form':
            pass
        elif request.POST['type'] == 'add_spend':
            return redirect('add_spend')


def spends_actions(request):
    if request.method == 'POST':
        spend_id = request.POST['spend_id']
        if request.POST['type'] == 'edit':
            user_id = Users.objects.get(id=request.session['user_id'])
            spends = Spends.objects.filter(user_id=user_id).order_by('-date')

            previous_data = {
                'description': request.POST['previous_desc'],
                'amount': request.POST['previous_amount'],
                'category': None if request.POST['previous_category'] == 'None'
                else Categories.objects.get(name=request.POST['previous_category']).id,
                'date': request.POST['previous_date'],
            }

            form = EditSpendForm(previous_data)

            return render(request, 'spends/index.html', context={'view_form': form, 
                                                                 'edited_field': int(spend_id), 
                                                                 'view_spends': True,
                                                                 'all_spends': spends,
                                                                 })
        elif request.POST['type'] == 'delete':
            Spends.objects.filter(id=spend_id).delete()

            category = Categories.objects.get(id=request.POST['category'])
            category.update_category_amount()

            return redirect('main')
        elif request.POST['type'] == 'save':
            Spends.objects.filter(id=spend_id).update(
                desc=request.POST['description'],
                amount=request.POST['amount'],
                category=request.POST['category'],
                date = f'{request.POST['date_year']}-{request.POST['date_month']}-{request.POST['date_day']}',
                )
            
            if request.POST['category'] != '':
                category = Categories.objects.get(id=request.POST['category'])
                category.update_category_amount()

            return redirect('main')
        elif request.POST['type'] == 'esc':
            return redirect('main')
    else:
        return redirect('main')


def view_all_categories(request):
   if 'user_id' in request.session:
        user_id = Users.objects.get(id=request.session['user_id'])
        categories = Categories.objects.filter(user_id=user_id)

        return render(request, 'spends/all_categories.html', {
            'view_categories': categories.exists(),
            'all_categories': categories,
        })
   else:
       return redirect('login')
   

def categories_actions(request):
    if request.method == 'POST':
        category_id = request.POST['category_id']
        if request.POST['type'] == 'edit':
            user_id = Users.objects.get(id=request.session['user_id'])
            categories = Categories.objects.filter(user_id=user_id)

            previous_data = {
                'name': request.POST['previous_name'],
            }

            form = EditCategoryForm(previous_data)

            return render(request, 'spends/all_categories.html', context={'view_form': form, 
                                                                 'edited_category': int(category_id), 
                                                                 'view_categories': True,
                                                                 'all_categories': categories,
                                                                 })
        elif request.POST['type'] == 'delete':
            Categories.objects.filter(id=category_id).delete()
            return redirect('all_categories')
        elif request.POST['type'] == 'save':
            Categories.objects.filter(id=category_id).update(
                name=request.POST['name'],
            )
            return redirect('all_categories')
        elif request.POST['type'] == 'esc':
            return redirect('all_categories')
    else:
        return redirect('main')



