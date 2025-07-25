from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get an item from a dictionary by key.
    Usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key, 0)

@register.filter
def split(value, delimiter):
    """
    Template filter to split a string by delimiter.
    Usage: {{ value|split:delimiter }}
    """
    return value.split(delimiter)

@register.filter
def trim(value):
    """
    Template filter to trim whitespace from a string.
    Usage: {{ value|trim }}
    """
    return value.strip() if value else value

@register.filter
def mul(value, arg):
    """
    Template filter to multiply two values.
    Usage: {{ value|mul:arg }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """
    Template filter to divide two values.
    Usage: {{ value|div:arg }}
    """
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0