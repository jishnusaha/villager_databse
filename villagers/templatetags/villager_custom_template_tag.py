from django import template
from urllib.parse import urlencode, quote
register = template.Library()

from time import sleep
@register.simple_tag(takes_context=True)
def replace_query_parameter(context, field, value):
    # print("in replace")
    # print(context['request'].get_full_path)
    # print("f: ", field, "v: ", value)
    dict_ = context['request'].GET.copy()
    dict_[field] = value
    return urlencode(dict_, quote_via=quote)


@register.simple_tag(takes_context=True)
def remove_query_parameter(context, field):
    dict_ = context['request'].GET.copy()
    del dict_[field]
    return urlencode(dict_, quote_via=quote)


# @register.simple_tag(takes_context=True)
# def prepare_login_url(context):
#     print()
#     print("in preprare")
#     dict_ = dict(context['request'].GET.copy())
#     d = {}
#     for key in dict_:
#         d[key]=dict_[key][0]
#     print(d)
#     print(urlencode(d, quote_via=quote))
#     print()
#     return urlencode(d, quote_via=quote)





