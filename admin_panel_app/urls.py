"""
URL configuration for admin_panel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin_hr/', views.IndexMainPage.as_view(), name='admin_hr'),
    path('admin_he/new_employee/', views.RegistrationNewUser.as_view(), name='new_employee'),
    path('admin_hr/all_employee/', views.AllEmployeeView.as_view(), name='all_employee'),
    path('admin_hr/change/<int:pk>', views.EditEmployee.as_view(), name = 'edit_employee')
]
