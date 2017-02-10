from django import template
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django.core.urlresolvers import NoReverseMatch, reverse


register = template.Library()

@register.simple_tag
def optional_singin(request):
    """
    Include a singin snippet if REST framework's singin view is in the URLconf.
    """
    try:
        singin_url = reverse('singin')
    except NoReverseMatch:
        return ''

    snippet = "<li><a href='{href}?next={next}'>Sing up</a></li>"
    snippet = format_html(snippet, href=singin_url, next=escape(request.path))
    return mark_safe(snippet)

@register.simple_tag
def optional_login(request):
    """
    Include a login snippet if REST framework's login view is in the URLconf.
    """
    try:
        login_url = reverse('rest_framework:login')
    except NoReverseMatch:
        return ''

    snippet = "<li><a href='{href}?next={next}'>Sing in</a></li>"
    snippet = format_html(snippet, href=login_url, next=escape(request.path))

    return mark_safe(snippet)