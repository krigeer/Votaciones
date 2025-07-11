from django.shortcuts import render, redirect   


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def gestor(request):
    return render(request, 'appGestor/panel.html')

def candidatos(request):
    return render(request, 'candidatos.html')