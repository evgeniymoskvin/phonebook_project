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
    path('admin_hr/new_employee/', views.RegistrationNewUser.as_view(), name='new_employee'),
    path('admin_hr/all_employee/', views.AllEmployeeView.as_view(), name='all_employee'),
    path('admin_hr/change/<int:pk>', views.EditEmployee.as_view(), name='edit_employee'),
    path('admin_hr/ajax/username_exists/', views.username_exists, name='username_exists'),
    path('admin_hr/all_groupdep/', views.AllDepGroupView.as_view(), name='all_groupdep'),
    path('admin_hr/new_groupdep/', views.AddNewGroupDepView.as_view(), name='new_groupdep'),
    path('admin_hr/change_groupdep/<int:pk>/', views.EditGroupDepView.as_view(), name='edit_groupdep'),
    path('admin_hr/all_command/', views.AllDepView.as_view(), name='all_dep'),
    path('admin_hr/new_command/', views.AddNewDepView.as_view(), name='new_dep'),
    path('admin_hr/change_command/<int:pk>', views.EditCommandView.as_view(), name='edit_dep'),
    path('admin_hr/ajax/translate_name', views.translate_name, name='translate_name'),
    path('admin_hr/service/all_emp_info/', views.ServiceInfoView.as_view(), name='all_info'),
]
