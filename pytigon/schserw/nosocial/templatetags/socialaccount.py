from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def provider_login_url(context, provider, **params):
    return ""


@register.simple_tag(takes_context=True)
def providers_media_js(context):
    return ""


@register.simple_tag
def get_social_accounts(user):
    return {}


@register.simple_tag(takes_context=True)
def get_providers(context):
    return []
