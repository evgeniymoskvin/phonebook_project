import os
import re
import time
import logging
from django.conf import settings
from django.core.mail import EmailMessage

from .models import MoreDetailsEmployeeModel, EmployeeModel

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")


def send_employees_salary_blank(results_people):
    """Функция отправки письма с расчетным листком на почту"""
    for one_employee in results_people:
        time.sleep(1)  # Делаем паузу для отправки сообщений
        text = one_employee  # Достаем текст по каждому сотруднику
        match_number = re.findall(r"Табельный номер:\s\s(.*?)\s", text, re.DOTALL)  # Достаем табельный номер сотрудника
        print(f'Табельный номер: {match_number[0]}')
        logging.info(f'Табельный номер: {match_number[0]}')
        month_name = re.findall(r"з/платы за\s(.*?)\n", text, re.DOTALL)  # Достаем месяц и год
        try:
            # Находим сотрудника с таким табельным номером
            emp_to_send = EmployeeModel.objects.get(personnel_number=match_number[0])
            print(f'Сотрудник: {emp_to_send}')
            logging.info(f'Сотрудник: {emp_to_send}')
            # Находим дополнительную информацию по нему
            more_info_of_emp = MoreDetailsEmployeeModel.objects.get(emp=emp_to_send)
            # Если подписано согласие на отправку расчетных листков
            if more_info_of_emp.send_email_salary_blank is True:
                email_to_emp = EmailMessage(f'Расчетный листок за {month_name[0]}',
                                            f'{emp_to_send}, Ваш расчетный листок за {month_name[0]} во вложении',
                                            to=[emp_to_send.user.email])
                # Формируем приложенный файл
                email_to_emp.attach(f'{match_number[0]}-{month_name[0]}.txt', text, mimetype='text/plain')
                email_to_emp.send()
                logging.info(f"Письмо отправлено: {emp_to_send}")
                print(f'Письмо отправлено: {emp_to_send}')
            else:
                # Если согласие на отправку расчетных листков не подписано
                logging.info(f'Запрет на отправку письма: {emp_to_send}')
                print(f'Запрет на отправку письма: {emp_to_send}')
        except Exception as e:
            logging.warning(f"Сотрудник {match_number} не найден: {e}")
            print(f"Сотрудник {match_number} не найден: {e}")
    return True
