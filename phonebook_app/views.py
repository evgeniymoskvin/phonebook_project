from django.shortcuts import render
from django.views import View
from .models import EmployeeModel, MoreDetailsEmployeeModel, User
from .forms import FilterForm
# Create your views here.

class IndexPageView(View):
    def get(self, request):
        employees = EmployeeModel.objects.get_queryset().filter(work_status=True).order_by('last_name', 'first_name', 'middle_name')
        dep_form = FilterForm()
        content = {
            'employees': employees,
            'dep_form': dep_form,
        }
        return render(request, 'phonebook_app/index.html', content)


def get_grid_view(request):
    dep_field = request.GET.get('dep_field')
    if dep_field:
        employees = EmployeeModel.objects.get_queryset().filter(work_status=True).filter(department_group_id=dep_field).order_by('last_name', 'first_name',
                                                                                           'middle_name')
    else:
        employees = EmployeeModel.objects.get_queryset().filter(work_status=True).order_by('last_name', 'first_name',
                                                                                           'middle_name')

    count = employees.count()
    content = {
        'count': count,
        'employees': employees}
    return render(request, 'phonebook_app/grid_view.html', content)

def get_list_view(request):
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
    request_emp_id = request.GET.get('emp_id')
    emp = EmployeeModel.objects.get(id=request_emp_id)
    user_info = User.objects.get(id=emp.user_id)
    print(emp)
    try:
        more_details = MoreDetailsEmployeeModel.objects.get(emp_id=request_emp_id)
    except:
        more_details = None
    print(more_details)
    content = {
        'emp': emp,
        'more_details': more_details,
        'user_info': user_info
    }
    return render(request, 'phonebook_app/modal_fade_details.html', content)