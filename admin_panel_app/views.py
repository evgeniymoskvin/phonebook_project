from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import View

from django.utils.decorators import method_decorator
from django.utils.encoding import escape_uri_path
from django.conf import settings
from django.contrib.auth import authenticate, login

from .forms import MoreDetailsEmployeeForm, EmployeeForm, UserRegistration
from .models import MoreDetailsEmployeeModel, EmployeeModel, CanEditEmployee


class IndexMainPage(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        employees = EmployeeModel.objects.get_queryset().order_by('last_name')
        det = MoreDetailsEmployeeModel.objects.get_queryset()
        for obj in det:
            try:
                print(obj.photo.url)
            except:
                print("no photo")
        content = {
            'count_emp': employees.count(),
            'count_work_emp': employees.filter(work_status=True).count(),
            'count_not_work_emp': employees.filter(work_status=False).count(),
            'det': det,
            'permission': check_user}
        return render(request, 'admin_panel_app/index.html', content)


class AllEmployeeView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        employees = EmployeeModel.objects.get_queryset().order_by('last_name')
        content = {
            'employees': employees,
            'permission': check_user}
        return render(request, 'admin_panel_app/all_employee.html', content)


class RegistrationNewUser(View):
    """Страница регистрации сотрудника"""

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        emp_form = EmployeeForm()
        more_details = MoreDetailsEmployeeForm()
        new_user = UserRegistration()
        content = {'emp_form': emp_form,
                   'more_details': more_details,
                   'new_user': new_user,
                   'permission': check_user}
        return render(request, 'admin_panel_app/new_employee.html', content)

    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        print(request.POST)
        user_form = UserRegistration(request.POST)
        new_user = None
        new_employee = None
        new_details = None
        # оздание логин/пароль нового сотрудника
        print(user_form.errors)
        if user_form.is_valid():
            new_user = User()
            new_user.username = request.POST.get('username')
            new_user.password = request.POST.get('password1')
            # new_user.password = request.POST.get('password2')
            new_user.email = request.POST.get('email')
            new_user.save()
            print(new_user)
            print(new_user.id)
        # Создание записи в таблице Сотрудники
        employee_form = EmployeeForm(request.POST)
        print(employee_form.errors)
        if employee_form.is_valid():
            new_employee = employee_form.save(commit=False)
            new_employee.user_id = new_user.id
            employee_form.save()
            print(new_employee.id)
        # Создание записи в таблице Дополнительная информация
        details_form = MoreDetailsEmployeeForm(request.POST, request.FILES)
        if details_form.is_valid():
            new_details = details_form.save(commit=False)
            new_details.emp_id = new_employee.id
            # new_details.photo = request.FILES['photo']
            details_form.save()

        # if request.FILES:
        #     """Копирование списка файлов"""
        #     list_copy_files = request.FILES.getlist('photo')
        #     for f in list_copy_files:
        #         obj = MoreDetailsEmployeeModel.objects.get(id=new_details.emp_id)
        #         obj.photo = f
        #         obj.save()

        print(new_user, new_employee, new_details)
        return redirect('new_employee')


class EditEmployee(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        emp = EmployeeModel.objects.get(id=pk)
        emp_form = EmployeeForm(instance=emp)
        try:
            more_det = MoreDetailsEmployeeModel.objects.get(emp_id=emp.id)
            more_details = MoreDetailsEmployeeForm(instance=more_det)
        except:
            more_details = MoreDetailsEmployeeForm()
        # user = User.objects.get(id=emp.user_id)

        content = {
            'emp_form': emp_form,
            'more_details': more_details,
            'permission': check_user}
        return render(request, 'admin_panel_app/edit_employee.html', content)

    @method_decorator(login_required(login_url='login'))
    def post(self, request, pk):
        employee_form = EmployeeForm(request.POST)
        details_form = MoreDetailsEmployeeForm(request.POST, request.FILES)
        emp = EmployeeModel.objects.get(id=pk)
        more_information_emp = MoreDetailsEmployeeModel.objects.get(emp_id=emp.id)
        more_information_emp.photo = request.FILES['photo']
        more_information_emp.save()
        # if employee_form.is_valid():
        #     employee = employee_form.save(commit=False)
        #     employee.user_id = emp.id
        #     employee_form.save()
        # try:
        #     more_information_emp = MoreDetailsEmployeeModel.objects.get(emp_id=emp.id)
        #     if details_form.is_valid():
        #         details = details_form.save(commit=False)
        #         details.id = more_information_emp.id
        #         details_form.save()
        # except:
        #     more_information = MoreDetailsEmployeeModel(emp_id=emp.id)
        #     if details_form.is_valid():
        #         details = details_form.save(commit=False)
        #         details.emp_id = emp.id
        #         details_form.save()
        # print(emp)
        # print(more_information)
        return redirect('all_employee')

def username_exists(request):
    username = request.GET.get('username')
    print(username)
    if User.objects.filter(username=username).exists():
        username_back = True
    else:
        username_back = False
    content = {
        'username_back': username_back
    }
    return render(request, 'admin_panel_app/ajax/ajax_username.html', content)