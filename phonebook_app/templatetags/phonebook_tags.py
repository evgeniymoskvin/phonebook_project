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
    except:
        url = f'/static/phonebook_app/icons/Group40.svg'
    return url


@register.simple_tag()
def get_days_to_birthday(emp_hb):
    try:
        hb_in_this_year = date(date.today().year, emp_hb.month, emp_hb.day)
        delta = hb_in_this_year - date.today()
        if delta.days > 0:
            return delta.days
        else:
            hb_in_next_year = date(date.today().year+1, emp_hb.month, emp_hb.day)
            print(hb_in_next_year)
            delta = abs(hb_in_next_year - date.today())
            return delta.days
    except:
        return None
