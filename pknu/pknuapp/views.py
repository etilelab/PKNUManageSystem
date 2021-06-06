from django.shortcuts import render

# Create your views here.


def index(request):
    res_data = {'test':'test'}
    return render(request, 'index.html', res_data)


def login(request):
    res_data = {'test':'test'}
    return render(request, 'login.html', res_data)


def logout(request):
    res_data = {'test':'test'}
    return render(request, 'index.html', res_data)


def register(request):
    res_data = {'test':'test'}
    return render(request, 'index.html', res_data)