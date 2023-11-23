from datetime import date

from django import template
from django.shortcuts import render, redirect
from ..models import *

register = template.Library()


@register.simple_tag()
def get_photo_url(user_id):
    try:
        det = MoreDetailsEmployeeModel.objects.get(emp_id=user_id)
        url = det.photo.url
        return '+'
    except:
        url = f'/static/phonebook_app/icons/Group40.svg'
        return '-'


@register.simple_tag()
def get_days_to_birthday(emp_hb):
    try:
        hb_in_this_year = date(date.today().year, emp_hb.month, emp_hb.day)
        delta = hb_in_this_year - date.today()
        if delta.days > 0:
            return delta.days
        else:
            hb_in_next_year = date(date.today().year + 1, emp_hb.month, emp_hb.day)
            # print(hb_in_next_year)
            delta = abs(hb_in_next_year - date.today())
            return delta.days
    except:
        return None


@register.simple_tag()
def get_month_name(date_hb):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    return f'{date_hb.day} {months[date_hb.month-1]}'


@register.simple_tag()
def get_birthday(emp_hb):
    try:
        hb = MoreDetailsEmployeeModel.objects.get(emp=emp_hb)
        return hb.date_birthday
    except:
        return '-'

@register.simple_tag()
def get_outside_email(emp):
    try:
        more_inf = MoreDetailsEmployeeModel.objects.get(emp=emp)
        return more_inf.outside_email
    except:
        return '-'

@register.simple_tag()
def get_room(emp):
    try:
        more_inf = MoreDetailsEmployeeModel.objects.get(emp=emp)
        return more_inf.room
    except:
        return '-'

@register.simple_tag()
def get_mobile_phone(emp):
    try:
        more_inf = MoreDetailsEmployeeModel.objects.get(emp=emp)
        return more_inf.mobile_phone
    except:
        return '-'

@register.simple_tag()
def get_city_emp(emp):
    try:
        more_inf = MoreDetailsEmployeeModel.objects.get(emp=emp)
        return more_inf.city_dep.city
    except:
        return '-'
