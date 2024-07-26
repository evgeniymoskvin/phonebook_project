import datetime
import mimetypes
import xml.etree.ElementTree as ET
import os
import re


from django.http import JsonResponse, HttpResponse
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
from django.core.mail import EmailMessage

from .forms import MoreDetailsEmployeeForm, EmployeeForm, UserRegistration, NewGroupDepForm, NewCommandForm, \
    UploadFileForm
from .models import MoreDetailsEmployeeModel, EmployeeModel, CanEditEmployee, GroupDepartmentModel, CommandNumberModel, \
    CityDepModel
from .functions import check_permission_user, add_stats_work_people
from .email_functions import send_employees_salary_blank
from .tasks import celery_send_employees_salary_blank




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
        add_stats_work_people(new_employee)
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
        print(request.POST)
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
            add_stats_work_people(emp)
        # Заполняем таблицу дополнительной информации
        details_form = MoreDetailsEmployeeForm(request.POST, request.FILES)

        more_information_emp = None
        try:
            more_information_emp = MoreDetailsEmployeeModel.objects.get(emp_id=emp.id)
        except Exception as e:
            print(f'MoreDetailsEmployeeModel.objects.get: {e}')
            more_information_emp = MoreDetailsEmployeeModel(emp_id=emp.id)
        try:
            more_information_emp.photo = request.FILES['photo']
        except Exception as e:
            print(f'Photo exception: {e}')
        try:
            more_information_emp.outside_email = details_form.data['outside_email']
        except Exception as e:
            print(f'Photo exception: {e}')
        try:
            more_information_emp.mobile_phone = details_form.data['mobile_phone']
        except Exception as e:
            print(f'Photo exception: {e}')
        try:
            # Проверка правильности записи дня рождения
            if datetime.date.fromisoformat(details_form.data['date_birthday']):
                more_information_emp.date_birthday = details_form.data['date_birthday']
        except Exception as e:
            print(f'Проверка дня рождения: {e}')
        more_information_emp.room = details_form.data['room']
        more_information_emp.city_dep_id = details_form.data['city_dep']
        try:
            if employee_form.data['date_birthday_show'] == 'on':
                more_information_emp.date_birthday_show = True
        except:
            more_information_emp.date_birthday_show = False
        try:
            if employee_form.data['send_email_salary_blank'] == 'on':
                more_information_emp.send_email_salary_blank = True
        except:
            more_information_emp.send_email_salary_blank = False
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

    @method_decorator(login_required(login_url='login'))
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


class ServiceInfoView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        employees = EmployeeModel.objects.get_queryset().filter(work_status=True).order_by('last_name', 'first_name',
                                                                                           'middle_name')
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False
        content = {
            'permission': check_user,
            'employees': employees,
        }
        return render(request, 'admin_panel_app/service/all_emp_info.html', content)


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


def translate_name(request):
    """ajax функция перевода имени пользователя"""
    input_str = request.GET.get('str')
    output_str = translit(input_str, 'ru', reversed=True)
    output_str = output_str.replace("'", "")  # Убираем смягчения
    output_str = output_str.replace(" ", "")  # Убираем пробелы
    print(output_str)
    content = {
        'output_str': output_str
    }
    return JsonResponse(content, status=200, content_type="application/json")


class GetEmployeeListView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False

        cities = CityDepModel.objects.get_queryset().order_by('city')
        content = {
            'permission': check_user,
            'cities': cities,
        }
        return render(request, 'admin_panel_app/service/get_emp_list.html', content)


# Функции выгрузки данных по сотрудникам

def get_group_dep(request):
    cities = request.POST.getlist('city')
    group_deps = GroupDepartmentModel.objects.get_queryset().filter(city_dep__in=cities).filter(show=True).order_by(
        'group_dep_abr')
    content = {
        'group_deps': group_deps,
    }
    return render(request, 'admin_panel_app/service/form_checkboxes/check_group_dep.html', content)


def get_commands(request):
    group_deps = request.POST.getlist('group_dep')
    commands = CommandNumberModel.objects.get_queryset().filter(department__in=group_deps).filter(show=True).order_by(
        'command_number')
    content = {
        'commands': commands,
    }
    return render(request, 'admin_panel_app/service/form_checkboxes/check_commands.html', content)
    # return JsonResponse(content, status=200, content_type="application/json")


def get_employees(request):
    commands = request.POST.getlist('command')
    emp = EmployeeModel.objects.get_queryset().filter(work_status=True).filter(department__in=commands).order_by(
        'last_name', 'first_name')
    content = {
        'emps': emp
    }
    return render(request, 'admin_panel_app/service/form_checkboxes/check_employees.html', content)


def get_columns(request):
    content = {
    }
    return render(request, 'admin_panel_app/service/form_checkboxes/check_columns.html', content)


def get_employees_list(request):
    columns = request.POST.getlist('column_checkbox')
    del columns[-1]
    fio_flag = False
    personnel_number_flag = False
    group_dep_abr_flag = False
    group_dep_flag = False
    command_number_flag = False
    command_name_flag = False
    job_title_flag = False
    birthday_flag = False
    phone_flag = False
    mobile_phone_flag = False
    email_flag = False
    email2_flag = False
    room = False
    login_flag = False
    for val in columns:
        if int(val) == 1:
            fio_flag = True
        if int(val) == 2:
            personnel_number_flag = True
        if int(val) == 3:
            group_dep_abr_flag = True
        if int(val) == 4:
            group_dep_flag = True
        if int(val) == 5:
            command_number_flag = True
        if int(val) == 6:
            command_name_flag = True
        if int(val) == 7:
            job_title_flag = True
        if int(val) == 8:
            birthday_flag = True
        if int(val) == 9:
            phone_flag = True
        if int(val) == 10:
            mobile_phone_flag = True
        if int(val) == 11:
            email_flag = True
        if int(val) == 12:
            email2_flag = True
        if int(val) == 13:
            room = True
        if int(val) == 14:
            login_flag = True
    employees = request.POST.getlist('employee')
    emps = EmployeeModel.objects.get_queryset().filter(id__in=employees)
    content = {
        'employees': emps,
        'fio_flag': fio_flag,
        'personnel_number_flag': personnel_number_flag,
        'group_dep_abr_flag': group_dep_abr_flag,
        'group_dep_flag': group_dep_flag,
        'command_number_flag': command_number_flag,
        'command_name_flag': command_name_flag,
        'job_title_flag': job_title_flag,
        'birthday_flag': birthday_flag,
        'phone_flag': phone_flag,
        'mobile_phone_flag': mobile_phone_flag,
        'email_flag': email_flag,
        'email2_flag': email2_flag,
        'room': room,
        'login_flag': login_flag,

    }
    return render(request, 'admin_panel_app/service/form_checkboxes/selected_emp_info.html', content)


class DownloadFileView(View):
    def get(self, request):
        first = ET.Element('YealinkIPPhoneDirectory')
        employees = EmployeeModel.objects.get_queryset().filter(work_status=True)
        for emp in employees:
            directory = ET.SubElement(first, 'DirectoryEntry')
            name = ET.SubElement(directory, 'Name')
            tel = ET.SubElement(directory, 'Telephone')
            name.text = f'{emp.last_name} {emp.first_name} {emp.middle_name}'
            tel.text = f'{emp.user_phone}'
        if not os.path.exists(os.path.join(settings.BASE_DIR, 'media', 'files', 'xml')):
            os.makedirs(os.path.join(settings.BASE_DIR, 'media', 'files', 'xml'))
        link_xml = os.path.join(settings.BASE_DIR, 'media', 'files', 'xml', 'xml.xml')
        ET.ElementTree(first).write(link_xml, encoding='utf-8-sig')
        with open(link_xml, 'rb') as f:
            mime_type, _ = mimetypes.guess_type(link_xml)
            response = HttpResponse(f.read(), content_type=mime_type)
        return response


def handle_upload_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


SMTP_SERVER = '161.11.16.20'
SMTP_PORT = 587
SMTP_USERNAME = 'print@el-spb.local'
SMTP_PASSWORD = 'Istok123'


class SendEmailSalaryBlankView(View):
    """Страница загрузки файла для рассылки расчетных листков сотрдникам"""
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        try:
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except:
            check_user = False

        content = {'form': UploadFileForm(),
                   'permission': check_user,
                   }
        return render(request, 'admin_panel_app/upload_file_to_send_salary.html', content)

    def post(self, request):
        print(f'request.POST: {request.POST}')
        print(f'request.FILES: {request.FILES}')
        money_list = request.FILES['file']
        temp_file_path = os.path.join(settings.MEDIA_ROOT, str(money_list.name))
        # Создаем физически файл
        with open(temp_file_path, "wb+") as dest_file:
            for chunk in money_list.chunks():
                dest_file.write(chunk)
            # Разбираем файл в список results_people
            re_pattern = re.compile(r"АО КИС(.*?)---\n\n\n\n\n", re.DOTALL)
            results_people = []
            with open(dest_file.name, encoding='cp1251') as f:
                for m in re_pattern.findall(f.read()):
                    results_people.append(f'АО КИС{m}')  #Добавляем отрезанные в начале буквы
            celery_send_employees_salary_blank.delay(results_people)
        # Удаляем загруженный файл
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        resp = HttpResponse(status=200)
        return resp
