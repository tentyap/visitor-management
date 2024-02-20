from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            print(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            next = request.GET.get('next')
            
            user = authenticate(request, username=username, password=password)
            if user is not None and user.check_password(password):
                login(request, user)
                if next:
                    return redirect(f'{next}')
                else:
                    return HttpResponseRedirect('/')
            else:
                messages.info(request, 'Username or password is incorrect.')
        return render(request, 'user/login.html')


@ensure_csrf_cookie
def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        print(request.POST)
        if request.method == "POST":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if username and email and password:
                if password == password2:
                    user = User.objects.create(
                        email=email,
                        username=username,
                    )
                    user.set_password(password)
                    user.save()

                    return redirect('/login')
                    # login(request, user)
                    # return redirect('/')
                else:
                    messages.error(request, "The two password fields didn'/t match.")
                    return HttpResponseRedirect('/register')
            else:
                messages.error(request, "All fields are required.")
                return HttpResponseRedirect('/register')
        
    return render(request,'user/register.html')

@ensure_csrf_cookie
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Logged out successfully!")
 
    return redirect("/login")

