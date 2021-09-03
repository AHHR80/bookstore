from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser


class MyUser_edit(admin.ModelAdmin):
    list_display = ['email', 'phone', 'data_join', 'last_login']
    search_fields = ['email', 'phone']

    readonly_fields = ['data_join', 'last_login']
 
 
admin.site.register(MyUser, MyUser_edit)
