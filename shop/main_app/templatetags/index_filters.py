from django import template

register = template.Library()


@register.filter(name='discount')
def get_discount(value):
    """The function to multiply the discount by 100"""

    return round(value * 100)
