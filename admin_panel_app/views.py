import datetime

from django.http import JsonResponse
from django.shortcuts import render

from transliterate import translit, get_available_language_codes

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

from .forms import MoreDetailsEmployeeForm, EmployeeForm, UserRegistration, NewGroupDepForm, NewCommandForm
from .models import MoreDetailsEmployeeModel, EmployeeModel, CanEditEmployee, GroupDepartmentModel, CommandNumberModel
from .functions import check_permission_user


class IndexMainPage(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):

        # try:
        #     user = EmployeeModel.objects.get(user=request.user)
        #     check_user = CanEditEmployee.objects.get(emp_id=user.id)
        # except:
        #     check_user = False
        employees = EmployeeModel.objects.get_queryset().order_by('last_name')
        group_dep = GroupDepartmentModel.objects.get_queryset()
        deps = CommandNumberModel.objects.get_queryset()
        permission = check_permission_user(request)
        content = {
            'count_emp': employees.count(),
            'count_work_emp': employees.filter(work_status=True).count(),
            'count_not_work_emp': employees.filter(work_status=False).count(),
            'group_dep': group_dep.count(),
            'group_dep_show': group_dep.filter(show=True).count(),
            'group_dep_not_show': group_dep.filter(show=False).count(),
            'deps': deps.count(),
            'deps_show': deps.filter(show=True).count(),
            'deps_not_show': deps.filter(show=False).count(),
        }
        content = {**permission, **content}
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
        return render(request, 'admin_panel_app/employee/all_employee.html', content)


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
        content = {'emp_form': emp_form,
                   'more_details': more_details,
                   'permission': check_user,
                   }
        return render(request, 'admin_panel_app/employee/new_employee.html', content)

    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        print(request.POST)
        user_form = UserRegistration(request.POST)
        new_user = None
        new_employee = None
        new_details = None
        # оздание логин/пароль нового сотрудника
        if user_form.is_valid():
            new_user = User.objects.create_user(email=request.POST.get('email'),
                                                username=request.POST.get('username'),
                                                password='Qwerty123!')

            # new_user.username = request.POST.get('username')
            # new_user.password = request.POST.get('password1')
            # new_user.password = 'Qwerty123!'

            # new_user.password = request.POST.get('password2')
            # new_user.email = request.POST.get('email')
            new_user.set_password('Qwerty123!')
            new_user.save()
            print(new_user)
            print(new_user.id)
        else:
            print(user_form.errors)
            content = {
                'error': user_form.errors
            }
            return render(request, 'admin_panel_app/ajax/error_list.html', content)
        # Создание записи в таблице Сотрудники
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            new_employee = employee_form.save(commit=False)
            new_employee.user_id = new_user.id
            employee_form.save()
            print(new_employee.id)
        else:
            print(employee_form.errors)
            content = {
                'error': employee_form.errors
            }
            return render(request, 'admin_panel_app/ajax/error_list.html', content)
        # Создание записи в таблице Дополнительная информация
        details_form = MoreDetailsEmployeeForm(request.POST, request.FILES)
        if details_form.is_valid():
            new_details = details_form.save(commit=False)
            new_details.emp_id = new_employee.id
            # new_details.photo = request.FILES['photo']
            details_form.save()
        else:
            print(details_form.errors)
            content = {
                'error': details_form.errors
            }
            return render(request, 'admin_panel_app/ajax/error_list.html', content)
        print(new_user, new_employee, new_details)
        return redirect('all_employee')


class EditEmployee(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        # Проверяем может ли пользователь редактировать сотрудников
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        # Заполняем поля из таблицы сотрудников
        emp = EmployeeModel.objects.get(id=pk)
        emp_form = EmployeeForm(instance=emp)
        # Заполняем если есть поля расширенной информации
        try:
            more_det = MoreDetailsEmployeeModel.objects.get(emp_id=emp.id)
            more_details = MoreDetailsEmployeeForm(instance=more_det)
        except:
            more_details = MoreDetailsEmployeeForm()
        user = User.objects.get(id=emp.user_id)
        new_user = UserRegistration(instance=user)

        content = {
            'emp_form': emp_form,
            'more_details': more_details,
            'permission': check_user,
            'new_user': new_user,
            'emp_id': emp.id,
            'login': emp.user}
        return render(request, 'admin_panel_app/employee/edit_employee.html', content)

    @method_decorator(login_required(login_url='login'))
    def post(self, request, pk):
        employee_form = EmployeeForm(request.POST)
        emp = EmployeeModel.objects.get(id=pk)
        if employee_form.is_valid():
            emp.last_name = employee_form.data['last_name']
            emp.first_name = employee_form.data['first_name']
            emp.middle_name = employee_form.data['middle_name']
            emp.personnel_number = employee_form.data['personnel_number']
            emp.job_title_id = employee_form.data['job_title']
            emp.department_id = employee_form.data['department']
            try:
                # Отсекаем все лишнее, кроме цифр
                user_phone = int(''.join(filter(str.isdigit, employee_form.data['user_phone'])))
                if user_phone != '':
                    # Если получилась не пустая строка
                    emp.user_phone = user_phone
            except Exception as e:
                print(e)
                emp.user_phone = None
            emp.department_group_id = employee_form.data['department_group']
            # Проверка права подписи
            try:
                if employee_form.data['right_to_sign'] == 'on':
                    emp.right_to_sign = True
            except:
                emp.right_to_sign = False
            # Проверка возможности редактировать
            try:
                if employee_form.data['check_edit'] == 'on':
                    emp.check_edit = True
            except:
                emp.check_edit = False
            # Проверка может ли выдавать задания
            try:
                if employee_form.data['can_make_task'] == 'on':
                    emp.can_make_task = True
            except:
                emp.can_make_task = False
            # Проверка ГИП
            try:
                if employee_form.data['cpe_flag'] == 'on':
                    emp.cpe_flag = True
            except:
                emp.cpe_flag = False
            # Получать рассылку
            try:
                if employee_form.data['mailing_list_check'] == 'on':
                    emp.mailing_list_check = True
            except:
                emp.mailing_list_check = False
            # Статут работы
            try:
                if employee_form.data['work_status'] == 'on':
                    emp.work_status = True
            except:
                emp.work_status = False
            emp.save()
        # Заполняем таблицу дополнительной информации
        details_form = MoreDetailsEmployeeForm(request.POST, request.FILES)
        if details_form.is_valid():
            more_information_emp = None
            try:
                more_information_emp = MoreDetailsEmployeeModel.objects.get(emp_id=emp.id)
            except:
                more_information_emp = MoreDetailsEmployeeModel(emp_id=emp.id)
            try:
                more_information_emp.photo = request.FILES['photo']
            except Exception as e:
                print(f'exception: {e}')
            more_information_emp.outside_email = details_form.data['outside_email']
            more_information_emp.mobile_phone = details_form.data['mobile_phone']
            try:
                # Проверка правильности записи дня рождения
                if datetime.date.fromisoformat(details_form.data['date_birthday']):
                    more_information_emp.date_birthday = details_form.data['date_birthday']
            except Exception as e:
                print(e)
            more_information_emp.room = details_form.data['room']
            more_information_emp.city_dep_id = details_form.data['city_dep']
            try:
                if employee_form.data['date_birthday_show'] == 'on':
                    more_information_emp.date_birthday_show = True
            except:
                more_information_emp.date_birthday_show = False
            more_information_emp.save()
        change_user = User.objects.get(id=emp.user_id)
        change_user.email = request.POST.get('email')
        change_user.save()
        return redirect('all_employee')


class AllDepGroupView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        all_groupdep = GroupDepartmentModel.objects.get_queryset().order_by('group_dep_abr')
        content = {'permission': check_user,
                   'all_groupdep': all_groupdep}
        return render(request, 'admin_panel_app/group_dep/all_groupdep.html', content)


class AddNewGroupDepView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        dep_form = NewGroupDepForm()
        content = {'permission': check_user,
                   'dep_form': dep_form,
                   'name_page': 'Добавить управление',
                   'button_text': 'Создать'}
        return render(request, 'admin_panel_app/group_dep/new_groupdep.html', content)

    def post(self, request):
        dep_form = NewGroupDepForm(request.POST)
        if dep_form.is_valid():
            dep_form.save()
        else:
            print(dep_form.errors)
            content = {
                'error': dep_form.errors
            }
            return render(request, 'admin_panel_app/ajax/error_list.html', content)
        return redirect('all_groupdep')


class EditGroupDepView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        dep = GroupDepartmentModel.objects.get(id=pk)
        dep_form = NewGroupDepForm(instance=dep)
        content = {'permission': check_user,
                   'dep_form': dep_form,
                   'name_page': 'Редактировать управление',
                   'button_text': 'Сохранить'}
        return render(request, 'admin_panel_app/group_dep/new_groupdep.html', content)

    def post(self, request, pk):
        dep_form = NewGroupDepForm(request.POST)
        if dep_form.is_valid():
            edit_dep = dep_form.save(commit=False)
            edit_dep.id = pk
            dep_form.save()

        else:
            print(dep_form.errors)
            content = {
                'error': dep_form.errors
            }
            return render(request, 'admin_panel_app/ajax/error_list.html', content)
        return redirect('all_groupdep')


class AllDepView(View):
    """Просмотр всех отделов"""

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        all_dep = CommandNumberModel.objects.get_queryset().order_by('command_number')
        content = {'permission': check_user,
                   'all_dep': all_dep}
        return render(request, 'admin_panel_app/command/all_dep.html', content)


class AddNewDepView(View):
    """Создание новых отделов"""
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        new_command_form = NewCommandForm()
        content = {'permission': check_user,
                   'new_command_form': new_command_form,
                   'name_page': 'Создать отдел',
                   'button_text': 'Создать',
                   }
        return render(request, 'admin_panel_app/command/new_command.html', content)

    def post(self, request):
        command_form = NewCommandForm(request.POST)
        if command_form.is_valid():
            command_form.save()
        else:
            print(command_form.errors)
            content = {
                'error': command_form.errors
            }
            return render(request, 'admin_panel_app/ajax/error_list.html', content)
        return redirect('all_dep')


class EditCommandView(View):
    """Редактирование отдела"""
    def get(self, request, pk):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        command = CommandNumberModel.objects.get(id=pk)
        command_form = NewCommandForm(instance=command)
        content = {'permission': check_user,
                   'new_command_form': command_form,
                   'name_page': 'Редактировать отдел',
                   'button_text': 'Сохранить'}
        return render(request, 'admin_panel_app/command/new_command.html', content)

    def post(self, request, pk):
        command = CommandNumberModel.objects.get(id=pk)
        command_form = NewCommandForm(request.POST)
        if command_form.is_valid():
            edit_command = command_form.save(commit=False)
            edit_command.id = command.id
            command_form.save()
            return redirect('all_dep')
        else:
            print(command_form.errors)
            content = {
                'error': command_form.errors
            }
            return render(request, 'admin_panel_app/ajax/error_list.html', content)


def username_exists(request):
    """ajax функция проверки существования пользователя"""
    username = request.GET.get('username')
    print(f'checking {username}')
    if User.objects.filter(username=username).exists():
        username_back = True
    else:
        username_back = False
    content = {
        'username_back': username_back
    }
    return render(request, 'admin_panel_app/ajax/ajax_username.html', content)

def translate_name (request):
    """ajax функция перевода имени пользователя"""
    input_str = request.GET.get('str')
    output_str = translit(input_str, 'ru', reversed=True)
    print(output_str)
    content = {
        'output_str': output_str
    }
    return JsonResponse(content, status=200, content_type="application/json")