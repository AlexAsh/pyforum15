from django.shortcuts import render
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect

from django.contrib import auth

from main.models import Comment

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if User.objects.filter(username=username):
            return render(request, 'register.html',
                    {'errors': 'This username is already taken'})

        user = User.objects.create_user(username=username, password=password)

        if user:
            user = auth.authenticate(username=username, password=password)
            auth.login(request,user)
            return HttpResponseRedirect("/forum")

        return render(request, str(user))
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect("/forum")
        else:
            return render(request, 'login.html', {'errors': 'Wrong login or username'})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/forum")

def forum(request):
    if request.method == "POST" and request.user.is_authenticated():
        parent = Comment.get_comment_by_id_string(request.POST["parent"])

        if parent:
            Comment.objects.create(text=request.POST["text"],
                                   user=request.user, parent=parent).save()
        else:
            Comment.objects.create(text=request.POST["text"], user=request.user).save()

    comments = Comment.objects.all()
    return render(request, 'forum.html', {'comments': comments})

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/forum")
    return HttpResponseRedirect("/login")
