
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('signup/',views.signup, name='signup'),
    path('login/',views.login,name='login'),
    path('login/signup/',views.signup, name='signup'),
    path('login/change_password', views.change_password, name="change_password"),
    path('login/forgetpassword/', views.forgetPassword, name='forgetpassword')
]
