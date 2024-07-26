import os
import datetime
import time
from django.core.mail import EmailMessage


from .models import EmployeeModel, MoreDetailsEmployeeModel

from phonebook_project.celery import app
from .email_functions import send_employees_salary_blank


@app.task()
def celery_send_employees_salary_blank(results_people):
    send_employees_salary_blank(results_people)
    return f'Рассылка расчетных листочков окончена'