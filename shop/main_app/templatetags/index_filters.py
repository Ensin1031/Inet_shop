from django import template


register = template.Library()


@register.filter(name='discount')
def get_discount(value):
    return round(value * 100)