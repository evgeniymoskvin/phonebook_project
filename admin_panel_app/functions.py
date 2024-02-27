from .models import EmployeeModel, CanEditEmployee, StatsEmployeeModel


def check_permission_user(request):
    try:
        user = EmployeeModel.objects.get(user=request.user)
        check_user = CanEditEmployee.objects.get(emp_id=user.id)
    except:
        check_user = False

    return {'permission': check_user}


def add_stats_work_people(emp):
    new_stat = StatsEmployeeModel()
    new_stat.employee = emp
    if emp.work_status is False:
        new_stat.employee_action = 0
    new_stat.count_people_in_company = EmployeeModel.objects.get_queryset().filter(work_status=True).count()
    new_stat.save()
    return None
