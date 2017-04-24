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

@register.simple_tag
def optional_logout(request, user):
    """
    Include a logout snippet if REST framework's logout view is in the URLconf.
    """
    try:
        logout_url = reverse('rest_framework:logout')
        change_password = reverse('change_password')
        account_delete = reverse('account_delete')
    except NoReverseMatch:
        snippet = format_html('<li class="navbar-text">{user}</li>', user=escape(user))
        return mark_safe(snippet)

    snippet = """<li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
            {user}
            <b class="caret"></b>
        </a>
        <ul class="dropdown-menu">
            <li><a href='{href}?next={next}'>Log out</a></li>
            <li><a href='{href_change_password}?next={next}'> Change Password </a></li>
            <li><a href='{href_account_delete}?next={next}'> Delete Account </a></li>
        </ul>
    </li>"""
    snippet = format_html(snippet, user=escape(user), href=logout_url, next=escape(request.path), 
    href_change_password=change_password, href_account_delete=account_delete)

    return mark_safe(snippet)
