from .models import EmployeeModel, CanEditEmployee

def check_permission_user(request):
    try:
        user = EmployeeModel.objects.get(user=request.user)
        check_user = CanEditEmployee.objects.get(emp_id=user.id)
    except:
        check_user = False

    return {'permission': check_user}