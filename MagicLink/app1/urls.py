from django.urls import path
from app1.views import loginview, validateview, dashboardview,logoutview

urlpatterns = [
    path('login',loginview, name='login'),
    path('validate',validateview, name='validate'),
    path('dashboard/',dashboardview, name='dashboard'),
    path('logout',logoutview, name='logout'),

]