from django.shortcuts import render

# Create your views here.


def index(request):
    res_data = {'test':'test'}
    return render(request, 'index.html', res_data)


def customers(request):
    res_data = {'test': '안녕 나는 규빈이라고해 '}






    return render(request, 'customers.html', res_data)


def statistics(request):
    pass

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        res_data = {}
        if not (username and password):
            res_data['error'] = 'Login failed'
        else:
            try:
                fcuser = ApdoUsers.objects.get(username=username)
                if check_password(password, fcuser.password):
                    request.session['user'] = fcuser.id
                    return redirect('/')

                else:
                    res_data['error'] = 'Login failed'
            except ApdoUsers.DoesNotExist:
                res_data['error'] = 'Login failed'
        return render(request, 'login.html', res_data)


def logout(request):
    res_data = {'test':'test'}
    return render(request, 'index.html', res_data)


def register(request):
    res_data = {'test':'test'}
    return render(request, 'index.html', res_data)