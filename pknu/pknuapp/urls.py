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
    path('detail',views.detail, name='detail'),
]