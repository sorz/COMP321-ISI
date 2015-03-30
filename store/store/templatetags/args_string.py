from django import template


register = template.Library()

POSSIBLE_ARGS = ['filter', 'sort', 'start', 'end', 'page']

@register.simple_tag(takes_context=True)
def args_string(context):
    """For pagination template, getting a clean and OCD-friendly URL.

    Render a string of key-value pairs like "?filter=keyword&page=3",
    only set and non-blank value will appear.
    """
    args = {key: context[key] for key in POSSIBLE_ARGS if context.get(key)}

    # Reference:
    # http://codereview.stackexchange.com/questions/7953/
    # how-do-i-flatten-a-dictionary-into-a-string
    s = '&'.join("{!s}={!s}".format(key, val) for (key, val) in args.items())
    if s:
        return '?' + s
    return ''
