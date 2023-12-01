from django.shortcuts import render
from django.views import View
# from .models import EmployeeModel, MoreDetailsEmployeeModel, User
from admin_panel_app.models import CanEditEmployee, MoreDetailsEmployeeModel, EmployeeModel, User
from .forms import FilterForm
import time
# Create your views here.

class IndexPageView(View):
    """Главная страница справочника"""

    def get(self, request):
        change_permission = False  # Права пользователя на редактирование сотрудников, для кнопки в хедере
        try:   # Проверяем авторизованного пользователя, если у него есть права редактирвоания, устанавливаем True
            user = EmployeeModel.objects.get(user=request.user)
            check_user = CanEditEmployee.objects.get(emp_id=user.id)
        except Exception as e:
            check_user = False
        # Получаем список работающих сотрудников
        employees = EmployeeModel.objects.get_queryset().filter(work_status=True).order_by('last_name', 'first_name', 'middle_name')
        dep_form = FilterForm()
        content = {
            'employees': employees,
            'dep_form': dep_form,
            'change_permission': check_user,
        }
        return render(request, 'phonebook_app/index.html', content)


def get_grid_view(request):
    """
    Функция для получения сотрудников в плиточном виде
    """
    # time.sleep(1)
    dep_field = request.GET.get('dep_field')
    if dep_field:
        employees = EmployeeModel.objects.get_queryset().filter(work_status=True).filter(department_group_id=dep_field).order_by('last_name', 'first_name',
                                                                                           'middle_name')
    else:
        employees = EmployeeModel.objects.get_queryset().filter(work_status=True).order_by('last_name', 'first_name',
                                                                                           'middle_name')

    count = employees.count()
    none_blocks = 6 - count % 6
    none_list = [i for i in range(none_blocks)]
    content = {
        'none_blocks': none_list,
        'count': count,
        'employees': employees}
    return render(request, 'phonebook_app/grid_view.html', content)



def get_list_view(request):
    """
    Функция для получения сотрудников в табличном (список) виде
    """
    # time.sleep(1)
    dep_field = request.GET.get('dep_field')
    if dep_field:
        employees = EmployeeModel.objects.get_queryset().filter(work_status=True).filter(department_group_id=dep_field).order_by('last_name', 'first_name',
                                                                                           'middle_name')
    else:
        employees = EmployeeModel.objects.get_queryset().filter(work_status=True).order_by('last_name', 'first_name',
                                                                                           'middle_name')
    content = {
        'employees': employees}
    return render(request, 'phonebook_app/table_view.html', content)

def get_details_modal_view(request):
    """
    Функция для отображения деталей по сотруднику
    """
    request_emp_id = request.GET.get('emp_id')
    emp = EmployeeModel.objects.get(id=request_emp_id)
    user_info = User.objects.get(id=emp.user_id)
    try:
        more_details = MoreDetailsEmployeeModel.objects.get(emp_id=request_emp_id)
    except Exception as e:
        print(e)
        more_details = None
    content = {
        'emp': emp,
        'more_details': more_details,
        'user_info': user_info
    }
    return render(request, 'phonebook_app/modal_fade_details.html', content)
