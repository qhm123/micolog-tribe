# coding: utf-8

from datetime import timedelta
from django import template
register = template.Library()

def timezone(value, offset):
    return value + timedelta(hours=offset)
register.filter(timezone)