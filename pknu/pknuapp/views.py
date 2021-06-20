from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import *
import json
from django.db.models import Q, Count
from datetime import datetime, timedelta
import time
from operator import itemgetter
from django.core.paginator import Paginator
from django.db.models.functions import Cast
from django.db import connections
import time
import datetime

# Create your views here.

def index(request):
    # 로그인 여부 확인
    user_id = request.session.get('user')
    if user_id:
        res_data = {'test':'test'}
        return render(request, 'index.html', res_data)
    else:
        redirect('/login')

def show_employee(request):
    user_id = request.session.get('user')
    if user_id:
        if request.method == 'GET':
            employees_data = Employees.objects.filter().values()
        elif request.method == "POST":
            e_email = request.POST.get('e_email', None)
            employees_data = Employees.objects.filter(Q(email=e_email)).values()

        e_pagenator = Paginator(employees_data, 10)
        ep = int(request.GET.get('ep', 1))
        employees = e_pagenator.get_page(ep)

        res_data = {
            'employees':employees,
            'employees_data':employees_data
        }
        return render(request, 'show_employee.html', res_data)

def show_item(request):
    user_id = request.session.get('user')
    product_name=""
    min_price=0
    max_price=999999

    if user_id:
        if request.method == 'GET':
            products_data = Products.objects.filter().values()
        elif request.method == "POST":
            max_price = request.POST.get('product_max', 99999)
            min_price = request.POST.get('product_min', 0)
            print("max",max_price)

            product_name = request.POST.get('product_name', None)
            if product_name != "" and max_price != "" and min_price != "":
                products_data = Products.objects.filter(Q(product_name=product_name) & Q(list_price__gte=min_price) &
                                                        Q(list_price__lte=max_price)).order_by('list_price').values()
            elif product_name != "" and max_price != "" and min_price != "":
                products_data = Products.objects.filter(
                    Q(product_name=product_name) & Q(list_price__gte=min_price) &
                    Q(list_price__lte=max_price)).order_by('list_price').values()
            elif product_name != "" and max_price != "" and min_price != "":
                products_data = Products.objects.filter(
                    Q(product_name=product_name) & Q(list_price__gte=min_price) &
                    Q(list_price__lte=max_price)).order_by('list_price').values()
            else:
                products_data = Products.objects.filter(Q(list_price__gte=min_price) &
                                                        Q(list_price__lte=max_price)).order_by('list_price').values()

        pagenator = Paginator(products_data, 10)
        p = int(request.GET.get('p', 1))
        products = pagenator.get_page(p)

        res_data = {
            'products':products,
            'products_data':products_data,
            'product_name':product_name,
            'product_min':min_price,
            'product_max':max_price,
        }
        return render(request, 'show_item.html', res_data)

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        res_data = {}
        if not (email and password):
            res_data['error'] = 'Login failed'
        else:
            try:
                fcuser = Member.objects.get(email=email)
                if check_password(password, fcuser.passwd):
                    request.session['user'] = fcuser.email
                    return redirect('/')
                else:
                    res_data['error'] = 'Login failed'
            except Member.DoesNotExist:
                res_data['error'] = 'Login failed'
        return render(request, 'login.html', res_data)


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['re_password']
        employee_id = request.POST['employee_id']
        res_data = {}
        if not (email and password and re_password):
            res_data['error'] = "Input all value"
        if password != re_password :
            res_data['error'] = 'Repeat Password '
        else:
            user = Member(email=email, passwd=make_password(password), employee_id=employee_id, created_at=datetime.datetime.now())
            user.save()
        return render(request, 'register.html', res_data)





def customers(request):
    user_id = request.session.get('user')
    if user_id:
        if request.method == 'GET':
            customers_data = Customers.objects.filter().values()
            e_pagenator = Paginator(customers_data, 10)
            ep = int(request.GET.get('ep', 1))
            customers = e_pagenator.get_page(ep)

            city_customers_data = Customers.objects.filter().values()
            c_pagenator = Paginator(customers_data, 10)
            ep = int(request.GET.get('ep', 1))
            customers = e_pagenator.get_page(ep)

            res_data = {
                'customers': customers,
                'customers_data': customers_data
            }

            return render(request, 'customers.html', res_data)

        elif request.method == 'POST':


            search = request.POST.get("search", None)
            city_search = request.POST.get("city_search", None)

            if search != None:
                customers_data = Customers.objects.filter(Q(name=search)).values()
            else:
                customers_data = Customers.objects.filter().values()

            if city_search != None:
                city_customers_data = Customers.objects.filter(Q(city=city_search)).values()
            else:
                city_customers_data = Customers.objects.filter().values()


            with connections["default"].cursor() as cursor:
                cursor.execute(
                    "select *from ("
                    "select name, status, order_id, salesman_id,"
                    "order_date from customers INNER JOIN orders ON customers.customer_id = orders.customer_id WHERE customers.customer_id = 1) a INNER JOIN"
                    " (select product_name, order_id from order_items INNER JOIN "
                    "products ON products.product_id = order_items.product_id) b ON a.order_id = b.order_id")
                row = cursor.fetchall()
            print(row)
            # [a,a,a,a,a,b,b,b,b,b,c,c,c,c,c,]
            # [ [a,a,a,a,a], [b,b,b,b,b,b,],[c,c,c,c,c]]
            e_pagenator = Paginator(customers_data, 10)
            ep = int(request.GET.get('ep', 1))
            customers = e_pagenator.get_page(ep)

            c_pagenator = Paginator(city_customers_data, 10)
            cp = int(request.GET.get('cp', 1))
            city_customers = c_pagenator.get_page(cp)

            res_data = {
                'customers':customers,
                'city_customers': city_customers,
                'customers_data':customers_data,
                'city_customers_data':city_customers_data,
                'city_search':city_search
            }

            return render(request, 'customers.html', res_data)




def statistics(request):
    pass