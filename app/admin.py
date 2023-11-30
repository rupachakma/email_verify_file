from django.contrib import admin
from app.models import Customuser
# Register your models here.

@admin.register(Customuser)
class CustomuserAdmin(admin.ModelAdmin):
    list_display = ['phone_num','email','is_superuser','is_staff']