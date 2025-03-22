from django import template

register = template.Library()

@register.filter
def get_choice(response, competence_number):
    if not response:
        return ""
    try:
        return getattr(response, f"choice_c{competence_number}")
    except AttributeError:
        return ""
