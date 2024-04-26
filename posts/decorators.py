from flask import redirect
from flask_login import current_user


def is_authenticated(func, redirect_url='/login'):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        return redirect(redirect_url)
    return wrapper
