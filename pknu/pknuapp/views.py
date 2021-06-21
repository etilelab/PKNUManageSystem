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
    try:
        user_id = request.session.get('user')
        if user_id:
            employee_id = Member.objects.get(email=user_id).employee_id
            manager_id = Employees.objects.get(employee_id=employee_id).manager_id

            print(manager_id)

            board = Board.objects.filter().order_by('-write_id').values()
            pagenator = Paginator(board, 10)
            p = int(request.GET.get('p', 1))
            boards = pagenator.get_page(p)
            res_data = {'user_id': user_id, 'manager_id':manager_id,'boards':boards}

            return render(request, 'index.html', res_data)

        return redirect('login')
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)

def detail_customerorders(request):
    try:
        user_id = request.session.get('user')
        if user_id:
            customer_id = request.GET.get('customer_id', None)
            customer_name = Customers.objects.get(customer_id=customer_id).name


            sql = "select *from (select name, customers.customer_id, status, order_id, salesman_id, order_date from customers INNER JOIN orders ON customers.customer_id = orders.customer_id) a INNER JOIN (select product_name, order_id from order_items INNER JOIN products ON products.product_id = order_items.product_id) b ON a.order_id = b.order_id where a.customer_id = " + str(customer_id)
            with connections["default"].cursor() as cursor:
                cursor.execute(sql)
                cus_order_detail = cursor.fetchall()

            res_data = {'cus_order_detail':cus_order_detail,'customer_name':customer_name, 'user_id':user_id}
            return render(request, 'detail_customerorders.html', res_data )
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)

def detail_customeritemcounts(request):
    try:
        user_id = request.session.get('user')
        if user_id:
            customer_id = request.GET.get('customer_id', None)
            customer_name = Customers.objects.get(customer_id=customer_id).name
            sql = "select customer_id, name, product_name, count(*) as counts from ((select name, customers.customer_id, status, order_id, salesman_id, order_date from customers INNER JOIN orders ON customers.customer_id = orders.customer_id) a INNER JOIN (select product_name, order_id from order_items INNER JOIN products ON products.product_id = order_items.product_id) b ON a.order_id = b.order_id) where customer_id=" + str(
                customer_id) + " group by product_name order by count(product_name) desc"

            with connections["default"].cursor() as cursor:
                cursor.execute(sql)
                cus_item_counts = cursor.fetchall()

            res_data = {'cus_item_counts': cus_item_counts,'customer_name':customer_name,'user_id':user_id}
            return render(request, 'detail_customeritemcounts.html', res_data)
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)
def show_customers(request):
    try:
        user_id = request.session.get('user')
        if user_id:
            if request.method == 'GET':
                customers_data = Customers.objects.filter().values()
                e_pagenator = Paginator(customers_data, 10)
                ep = int(request.GET.get('ep', 1))
                customers = e_pagenator.get_page(ep)

                city_customers_data = Customers.objects.filter().values()
                c_pagenator = Paginator(customers_data, 10)
                cp = int(request.GET.get('cp', 1))
                city_customers = c_pagenator.get_page(cp)

                res_data = {
                    'customers': customers,
                    'user_id':user_id,
                    'customers_data': customers_data,
                    'city_customers': city_customers,
                    'city_customers_data': city_customers_data
                }

                return render(request, 'show_customers.html', res_data)

            elif request.method == 'POST':
                search = request.POST.get("search", "")
                city_search = request.POST.get("city_search", "")

                if search != "":
                    customers_data = Customers.objects.filter(Q(name=search)).values()
                else:
                    customers_data = Customers.objects.filter().values()

                if city_search != "":
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
                    'search':search,
                    'city_search':city_search,
                    'user_id':user_id
                }

                return render(request, 'show_customers.html', res_data)
        return redirect('login')
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)
def write(request):
    try:
        # 로그인 여부 확인
        user_id = request.session.get('user')
        if user_id:
            employee_id = Member.objects.get(email=user_id).employee_id
            if request.method == 'GET':
                res_data = {'user_id': user_id}
                return render(request, 'write.html', res_data)
            elif request.method == 'POST':
                title = request.POST.get('title', "")
                content = request.POST.get('content', "")
                notice = request.POST.get('notice',"")

                if title != "" and content != "" and (notice == "0" or notice == "1"):
                    write_id = Board.objects.filter().order_by('-write_id').values()[0]['write_id']
                    sql = "insert into board values(" + str(int(write_id)+1) + ",'"+ title + "','"+ content + "'," + str(employee_id) + ",'" + str(datetime.datetime.now()) + "'," + str(notice) + ")"
                    with connections["default"].cursor() as cursor:
                        cursor.execute(sql)
                else:
                    redirect('write')

            return redirect('/')
        return redirect('login')
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)

def show_employee(request):
    try:
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
        else:
            return redirect('login')
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)

def show_item(request):
    try:
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
        else:
            return redirect('login')
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)

def detail(request):
    try:
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

            sql = "update products set views=views+1 where product_id=" + str(product_id)
            with connections["default"].cursor() as cursor:
                cursor.execute(sql)

            res_data = {'user_id': user_id,'product_detail':product_detail,'products':products}
            return render(request, 'detail.html', res_data)
        else:
            return redirect('login')
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)

def location(request):
    try:
        user_id = request.session.get('user')
        location_id = ""
        location_customer = ""
        if user_id:
            locations = Locations.objects.all()

            if request.method == "GET":
                sql = "select region_name, country_name, city, state, warehouse_name, product_name, quantity from inventories a, warehouses b , locations c, countries d, regions e, products f where a.product_id = f.product_id and a.warehouse_id = b.warehouse_id and b.location_id = c.location_id and d.country_id = c.country_id and e.region_id = d.region_id"
                with connections["default"].cursor() as cursor:
                    cursor.execute(sql)
                    location_data = cursor.fetchall()

            elif request.method == "POST":
                location_id = request.POST.get('hidden_location_id', "")
                if location_id != "" and location_id != "전체지역 (location)":
                    sql = "select region_name, country_name, city, state, warehouse_name, " \
                          "product_name, quantity from inventories a, warehouses b , locations c, countries d, regions e, products f " \
                          "where a.product_id = f.product_id and a.warehouse_id = b.warehouse_id and b.location_id = c.location_id and " \
                          "d.country_id = c.country_id and e.region_id = d.region_id and c.location_id="+str(location_id).split('-')[0]
                    with connections["default"].cursor() as cursor:
                        cursor.execute(sql)
                        location_data = cursor.fetchall()

                    sql = "select count(*) z, name, sum(unit_price*quantity), c.city from order_items a , orders b, customers c where a.order_id = b.order_id and c.customer_id = b.customer_id and city='" + str(location_id).split('-')[1] + "' group by c.customer_id order by z desc limit 10"
                    print(sql)
                    with connections["default"].cursor() as cursor:
                        cursor.execute(sql)
                        location_customer = cursor.fetchall()

                else:
                    sql = "select region_name, country_name, city, state, warehouse_name, product_name, quantity from inventories a, warehouses b , locations c, countries d, regions e, products f where a.product_id = f.product_id and a.warehouse_id = b.warehouse_id and b.location_id = c.location_id and d.country_id = c.country_id and e.region_id = d.region_id"
                    with connections["default"].cursor() as cursor:
                        cursor.execute(sql)
                        location_data = cursor.fetchall()


            pagenator = Paginator(location_data, 10)
            p = int(request.GET.get('p', 1))
            location_data_p = pagenator.get_page(p)

            res_data = {'user_id': user_id,'locations':locations,
                        'location_data_p':location_data_p,'hidden_location_id':location_id,'location_customer':location_customer}

            return render(request, 'location.html', res_data)
        else:
            return redirect('login')
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)

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
    try:
        if request.method == "GET":
            return render(request, 'register.html')
        elif request.method == "POST":
            try:
                email = request.POST['email']
                password = request.POST['password']
                re_password = request.POST['re_password']
                employee_id = request.POST['employee_id']
                res_data = {}
                if not (email and password and re_password):
                    res_data['error'] = "입력값에 문제가 있습니다."
                if password != re_password :
                    res_data['error'] = '비밀번호를 다시 입력해주세요'
                else:
                    user = Member(email=email, passwd=make_password(password), employee_id=employee_id, created_at=datetime.datetime.now())
                    user.save()
                    return redirect('login')
                return render(request, 'register.html', res_data)
            except:
                res_data = {'error':'error'}
                return render(request, 'error.html', res_data)
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)

def board(request):
    try:
        user_id = request.session.get('user')
        if user_id:
            write_id = request.GET.get('write_id', None)
            boards = Board.objects.get(Q(write_id=write_id))
            res_data = {
                'user_id': user_id,
                'board':boards
            }
            return render(request, 'board.html', res_data)
        else:
            return redirect('login')
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)

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
    if user_id:
        try:
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

                    message = "성공적으로 주문을 진행하였습니다. 구매완료! 남은 현금은 " + str(credit_limit) + "$ 입니다. 내 정보보기에서 구매내역을 확인하세요"
                elif quantity > remain_quantity:
                    message = "재고가 부족합니다."
                elif quantity*product_price > credit_limit:
                    message = "현금이 부족합니다. 현금을 추가로 결제해주세요. 현재 가지고있는 현금은 " + str(credit_limit) + "$ 입니다."
                else:
                    message = "주문에 실패하였습니다"

                res_data = {"message":message,'user_id':user_id}
            else:
                res_data = {"message":"에러 발생", 'user_id':user_id}
        except:
            res_data={'message':'에러 발생, 값을 제대로 입력하였는지 확인해주세요.'}
        return render(request, 'buy.html', res_data)
    else:
        return redirect('login')


def myinfo(request):
    try:
        user_id = request.session.get('user')
        if user_id:
            employee_id = Member.objects.get(email=user_id).employee_id

            if request.method == 'POST':
                cash = request.POST.get("charge_cash", 0)

                if int(cash) > 0:
                    sql = "update employees set credit_limit=credit_limit + " + str(cash) + " where employee_id=" + str(employee_id)
                    with connections["default"].cursor() as cursor:
                        cursor.execute(sql)

            employee = Employees.objects.get(employee_id=employee_id)
            sql ="select a.order_id, a.status, a.order_date, c.product_name, b.quantity, b.unit_price from orders a , order_items b, products c where a.employee_order=1 and  + a.salesman_id=" + str(employee_id) + " and a.order_id = b.order_id and c.product_id = b.product_id order by order_id desc limit 5"
            with connections["default"].cursor() as cursor:
                cursor.execute(sql)
                orders = cursor.fetchall()

            res_data = {"orders": orders, 'user_id': user_id,'employee':employee}

            return render(request, 'myinfo.html', res_data)
        return redirect('login')
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)

def customers(request):
    try:
        user_id = request.session.get('user')
        if user_id:
            if request.method == 'GET':
                customers_data = Customers.objects.filter().values()
                e_pagenator = Paginator(customers_data, 10)
                ep = int(request.GET.get('ep', 1))
                customers = e_pagenator.get_page(ep)

                res_data = {
                    'user_id': user_id,
                    'customers': customers,
                    'customers_data': customers_data,
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
                    'customers_data':customers_data,
                    'user_id':user_id,
                }

                return render(request, 'customers.html', res_data)
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)


def statistics(request):
    try:
        user_id = request.session.get('user')
        if user_id:

            sql = "select count(*), a.city from locations a , customers b where a.city = b.city group by a.city"
            with connections["default"].cursor() as cursor:
                cursor.execute(sql)
                customer_data = cursor.fetchall()

            location_customer_data = []
            location_customer_label = []
            for i in customer_data:
                location_customer_data.append(i[0])
                location_customer_label.append(i[1])

            sql = "select count(*), status from orders group by status"
            with connections["default"].cursor() as cursor:
                cursor.execute(sql)
                status_datas = cursor.fetchall()

            status_data = []
            status_label = []
            for i in status_datas:
                status_data.append(i[0])
                status_label.append(i[1])

            res_data = {
                'location_customer_data': json.dumps(location_customer_data),
                'location_customer_label': json.dumps(location_customer_label),
                'status_data': json.dumps(status_data),
                'status_label': json.dumps(status_label),
                'user_id':user_id
            }

            return render(request, 'statistics.html', res_data)
        return redirect('login')
    except:
        res_data = {'error': 'error'}
        return render(request, 'error.html', res_data)