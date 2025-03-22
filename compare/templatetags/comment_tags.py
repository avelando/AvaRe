from django import template

register = template.Library()

@register.filter
def get_comment(obj, idx):
    return getattr(obj, f"c{idx}", "")
