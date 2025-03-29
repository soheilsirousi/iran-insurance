from django.contrib import messages
from django.contrib.auth import logout


def admin_only(func):
    def wrapper(object, *args, **kwargs):
        if object.request.user.role == 3:
            logout(object.request)
            messages.error(object.request, "ورود به این صفحه برای مشتریان محدود است.")

        return func(object, *args, **kwargs)

    return wrapper
