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
from django.views.decorators.http import require_POST

# Create your views here.


def index(request):
    # 로그인 여부 확인
    user_id = request.session.get('user')
    if user_id:
        res_data = {'user_id': user_id}
        return render(request, 'index.html', res_data)

    return redirect('login')


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
            'employees_data':employees_data,
            'user_id': user_id,
        }

        return render(request, 'show_employee.html', res_data)


def show_item(request):
    user_id = request.session.get('user')
    product_name=""
    min_price= ""
    max_price=""
    category_id = ""

    if user_id:
        likes_products_data = Products.objects.filter().order_by('-likes').values()[:10]
        views_products_data = Products.objects.filter().order_by('-views').values()[:10]

        sql = "select * from (select product_id, count(*) customer_count from order_items group by product_id ) a INNER JOIN products ON products.product_id = a.product_id order by customer_count desc limit 10"
        with connections["default"].cursor() as cursor:
            cursor.execute(sql)
            customer_products = cursor.fetchall()

        if request.method == 'GET':
            products_data = Products.objects.filter().values()
            products_data2 = Products.objects.filter().values()
        elif request.method == "POST":

            max_price = request.POST.get('product_max', "")
            min_price = request.POST.get('product_min', "")
            category_id = request.POST.get('hidden_category_id',"")

            # 품목별 검색
            product_name = request.POST.get('product_name', "")
            if category_id == "1 (CPU)":
                products_data2 = Products.objects.filter(Q(category_id=1)).order_by('list_price').values()
            elif category_id == "2 (Video Card)":
                products_data2 = Products.objects.filter(Q(category_id=2)).order_by('list_price').values()
            elif category_id == "3 (Ram)":
                products_data2 = Products.objects.filter(Q(category_id=3)).order_by('list_price').values()
            elif category_id == "4 (Mother Board)":
                products_data2 = Products.objects.filter(Q(category_id=4)).order_by('list_price').values()
            elif category_id == "5 (Storage)":
                products_data2 = Products.objects.filter(Q(category_id=5)).order_by('list_price').values()
            else:
                products_data2 = Products.objects.filter().order_by('list_price').values()


            # 기타 검색
            if product_name != "" and max_price != "" and min_price != "":
                products_data = Products.objects.filter(Q(product_name=product_name) & Q(list_price__gte=min_price) &
                                                        Q(list_price__lte=max_price)).order_by('list_price').values()
            elif product_name == "" and max_price != "" and min_price != "":
                products_data = Products.objects.filter(
                    Q(list_price__gte=min_price) &
                    Q(list_price__lte=max_price)).order_by('-list_price').values()
            elif product_name != "" and max_price == "" and min_price == "":
                products_data = Products.objects.filter(
                    Q(product_name=product_name)).order_by('-list_price').values()
            else:
                products_data = Products.objects.filter().values()


        pagenator = Paginator(products_data, 10)
        p = int(request.GET.get('p', 1))
        products = pagenator.get_page(p)

        pagenator2 = Paginator(products_data2, 10)
        p2 = int(request.GET.get('p2', 1))
        products2 = pagenator2.get_page(p2)

        res_data = {
            'user_id': user_id,
            'products':products,
            'products2': products2,
            'products_data':products_data,
            'products_data2': products_data2,
            'product_name':product_name,
            'product_min':min_price,
            'product_max':max_price,
            'likes_products':likes_products_data,
            'views_products':views_products_data,
            'customer_products':customer_products,
            'hidden_category_id':category_id,
        }
        return render(request, 'show_item.html', res_data)


def detail(request):
    user_id = request.session.get('user')
    if user_id:
        product_id = request.GET.get('product_id', None)

        sql = "select * from (select * from (select product_id p, count(*) customer_count from order_items group by p ) a RIGHT JOIN products ON products.product_id = a.p) b INNER JOIN product_categories c ON c.category_id = b.category_id where b.product_id = " + str(product_id)
        with connections["default"].cursor() as cursor:
            cursor.execute(sql)
            product_detail = cursor.fetchall()[0]

        sql = "select * from inventories a , warehouses b, locations c where a.product_id = " + str(product_id) +" and a.warehouse_id = b.warehouse_id and c.location_id = b.location_id "
        with connections["default"].cursor() as cursor:
            cursor.execute(sql)
            products = cursor.fetchall()
        res_data = {'user_id': user_id,'product_detail':product_detail,'products':products}
        return render(request, 'detail.html', res_data)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        res_data = {}
        if not (email and password):
            res_data['error'] = '로그인 실패'
        else:
            try:
                fcuser = Member.objects.get(email=email)
                if check_password(password, fcuser.passwd):
                    request.session['user'] = fcuser.email
                    return redirect('/')
                else:
                    res_data['error'] = '로그인 실패'
            except Member.DoesNotExist:
                res_data['error'] = '로그인 실패'
        return render(request, 'login.html', res_data)


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('login')


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

def board(request):
    pass

@require_POST
def like(request):
    product_id = request.POST.get('productid', None)
    products_data = Products.objects.get(Q(product_id=product_id))
    products_data.likes = products_data.likes + 1
    products_data.save()
    likes = products_data.likes
    context = {'likes_count':likes}
    return HttpResponse(json.dumps(context), content_type="application/json")

def buy(request):
    user_id = request.session.get('user')
    employee_id = Member.objects.get(email=user_id).employee_id

    product_id = request.POST.get('productid', "")
    warehouse_name = request.POST.get('warehouse_name', "")
    product_price = request.POST.get('product_price', "")
    quantity = request.POST.get('quantity', "")

    if product_id != "" and warehouse_name != "" and product_price != "" and quantity != "":
        quantity = float(quantity)
        product_price = float(product_price)

        warehouse_id = Warehouses.objects.get(warehouse_name=warehouse_name).warehouse_id
        credit_limit = Employees.objects.get(employee_id=employee_id).credit_limit
        remain_quantity = float(Inventories.objects.get(Q(warehouse_id=warehouse_id) & Q(product_id=product_id)).quantity)

        if quantity < remain_quantity and quantity*product_price < credit_limit:
            buy_time = datetime.datetime.now()
            new_order_id = Orders.objects.all().order_by('-order_id')[0].order_id + 1

            Orders.objects.create(salesman_id =employee_id, status="Pending", employee_order=1, order_date=buy_time, order_id=new_order_id)
            OrderItems.objects.create(item_id =1, order_id=new_order_id, product_id=product_id, quantity=quantity, unit_price=product_price)

            sql = "update inventories set quantity=" + str(remain_quantity-quantity) + " where warehouse_id=" + str(warehouse_id) + " and product_id=" + str(product_id) + ""
            with connections["default"].cursor() as cursor:
                cursor.execute(sql)
            sql = "update employees set credit_limit=" + str(credit_limit - product_price) + " where employee_id=" + str(employee_id)
            with connections["default"].cursor() as cursor:
                cursor.execute(sql)


            message = "성공적으로 주문을 진행하였습니다. 구매완료!"
        elif quantity > remain_quantity:
            message = "재고가 부족합니다."
        elif quantity*product_price > credit_limit:
            message = "현금이 부족합니다. 현금을 추가로 결제해주세요. 현재 가지고있는 현금은 " + str(credit_limit) + "$ 입니다."
        else:
            message = "주문에 실패하였습니다"

        res_data = {"message":message,'user_id':user_id}

    return render(request, 'buy.html', res_data)


def customers(request):
    user_id = request.session.get('user')
    if user_id:
        if request.method == 'GET':
            customers_data = Customers.objects.filter().values()
            e_pagenator = Paginator(customers_data, 10)
            ep = int(request.GET.get('ep', 1))
            customers = e_pagenator.get_page(ep)

            res_data = {
                'customers': customers,
                'customers_data': customers_data
            }

            return render(request, 'customers.html', res_data)

        elif request.method == 'POST':
            search = request.POST.get("search", None)
            customers_data = Customers.objects.filter(Q(name=search)).values() # 100

            e_pagenator = Paginator(customers_data, 10)
            ep = int(request.GET.get('ep', 1))
            customers = e_pagenator.get_page(ep)
            res_data = {
                'customers':customers,
                'customers_data':customers_data
            }

            return render(request, 'customers.html', res_data)




    #elif request.method == 'POST':

        # customers_data = Customers.objects.filter().values()
        #
        # e_pagenator = Paginator(customers_data, 10)
        # ep = int(request.GET.get('ep', 1))
        # customers = e_pagenator.get_page(ep)


    # try:
    #     #fcuser = Member.objects.get(email=email)
    #
    #     if search_target == customers_data.name:
    #         #request.session['user'] = fcuser.email
    #         return redirect('/')
    #     else:
    #         #res_data['error'] = 'Login failed'
    # except Member.DoesNotExist:
    #     #res_data['error'] = 'Login failed'

        # res_data = {
        #     'customers' : customers,
        #     'customers_data' : customers_data
        # }




def statistics(request):
    pass