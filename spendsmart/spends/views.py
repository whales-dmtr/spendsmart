from django.http import HttpResponse
from django.shortcuts import render

def view_all_spends(HttpRequest):
    return render(HttpRequest, 'spends/index.html')