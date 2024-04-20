from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def code_block():
    return render_to_string('shared/code_block.html')