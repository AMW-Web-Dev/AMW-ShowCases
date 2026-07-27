import markdown as md_lib
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    md = md_lib.Markdown(extensions=["extra", "codehilite", "toc"])
    return mark_safe(md.convert(text))
