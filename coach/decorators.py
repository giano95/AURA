from functools import wraps
from django.core.exceptions import PermissionDenied


def coach_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_user_a_coach:
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper
