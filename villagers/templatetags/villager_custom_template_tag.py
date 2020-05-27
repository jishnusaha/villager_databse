from django import template
from urllib.parse import urlencode, quote
register = template.Library()

from time import sleep
@register.simple_tag(takes_context=True)
def replace_query_parameter(context, field, value):
    dict_ = context['request'].GET.copy()
    dict_[field] = value
    return urlencode(dict_, quote_via=quote)


@register.simple_tag(takes_context=True)
def remove_query_parameter(context, field):
    dict_ = context['request'].GET.copy()
    del dict_[field]
    return urlencode(dict_, quote_via=quote)

