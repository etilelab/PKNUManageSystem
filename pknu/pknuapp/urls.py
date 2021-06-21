from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('showemployee',views.show_employee, name='showemployee'),
    path('showitem',views.show_item, name='showitem'),
    path('login', views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('board',views.board, name='board'),
    path('like/',views.like, name='like'),
    path('buy/',views.buy, name='buy'),
    path('detail',views.detail, name='detail'),
    path('myinfo',views.myinfo, name='myinfo'),
    path('location',views.location, name='location'),
    path('write',views.write, name='write'),
path('showcustomers',views.show_customers, name='showcustomers'),
    path('detail_customerorders',views.detail_customerorders, name='detail_customerorders'),
    path('detail_customeritemcounts',views.detail_customeritemcounts, name='detail_customeritemcounts'),

]