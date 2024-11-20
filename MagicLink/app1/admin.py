from django.contrib import admin
from app1.models import UserData


# Register your models here.


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'email_verification_token', 'created_at']
