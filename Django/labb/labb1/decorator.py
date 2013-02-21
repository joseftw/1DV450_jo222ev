from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from functools import wraps
def login_required():
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            if not request.session["isLoggedIn"] == True:
              return redirect("login")
              
        return wraps(func)(inner_decorator)
    return decorator
