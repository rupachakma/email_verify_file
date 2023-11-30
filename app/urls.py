from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_user,name="register"),
    path('verify/', views.verify_account,name="verify"),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('',views.home,name="home")
]
