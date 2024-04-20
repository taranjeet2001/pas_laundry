from django.shortcuts import render

def check_authenticated(myfunc):
    def inner(request):
        if request.user.is_authenticated:
            resp=render(request,'LMS/home.html')
            return resp
        else:
            return myfunc(request)
    return inner
