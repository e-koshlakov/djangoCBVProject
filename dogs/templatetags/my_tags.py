from django import template

register = template.Library()


@register.filter
def my_media(value):
    if value:
        return fr'/media/{value}'
    return fr'/static/dummydog.jpg'
