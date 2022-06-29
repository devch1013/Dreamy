from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def minus(left, right):
   return round((round(float(left),3) - round(float(right),3)),3)

@register.filter
def plus(left, right):
   return float(left) + float(right)

@register.filter
def zip_list(a, b):
   if a != None:
      shop = str(a).split(',')
      link = str(b).split(',')
   else:
      shop = []
      link=[]
   return zip(shop, link)

@register.filter
def lessthan(left, right):
   return (round(float(left),3) < round(float(right),3))