import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def custom_markdown(value):
    res = mark_safe(markdown.markdown(value,
                                       extensions=['markdown.extensions.codehilite','markdown.extensions.fenced_code'],
                                       safe_mode=True,
                                       enable_attributes=False))
    return res
