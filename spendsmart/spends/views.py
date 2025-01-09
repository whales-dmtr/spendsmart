from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Spends, Categories
from .forms import AddSpendForm

def view_all_spends(HttpRequest):
    HttpRequest.session['is_logged_in'] = False
    print(HttpRequest.session['is_logged_in'])
    return render(HttpRequest, 'spends/index.html', {'all_spends': Spends.objects.all()})


def view_form_add_spend(HttpRequest):
    view_form = AddSpendForm()
    return render(HttpRequest, 'spends/add_spends.html', {'view_form': view_form})


def add_spend(HttpRequest):
    if HttpRequest.method == 'POST':
        desc = HttpRequest.POST['description']
        amount = HttpRequest.POST['amount']
        category = HttpRequest.POST['category']
        new_spend = Spends(
            user_id=4,
            desc=desc,
            amount=amount,
            category_id=category
        ) 
        new_spend.save()
    return redirect('main')




