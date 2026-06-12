from django import template

register = template.Library()


@register.filter
def startswith(path, arg):
    """Returns True if path starts with the given prefix."""
    return path.startswith(arg)