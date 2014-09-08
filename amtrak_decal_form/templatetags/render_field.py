from django import template

register = template.Library()


@register.simple_tag
def render_field(form, field_name):
    field = form[field_name]
    label_tag = field.label_tag()
    field_input = field
    return '%s%s' % (label_tag, field_input)
