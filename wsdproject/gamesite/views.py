from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        context = {'logouturl': '/logout', 'logout':'logout'}
        return render(request, "gamesite/index.html", context)
    else:
        context = {'loginurl': '/login', 'login':'login', 'registerurl':'/register', 'register':'register'}
        return render(request, "gamesite/index.html", context)

def register(request):
# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            name = form.cleaned_data['username']
            mail = form.cleaned_data['email']
            pw = form.cleaned_data['password']
            user = User.objects.create_user(username=name, email=mail, password=pw)
            user.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, 'gamesite/register.html', {'form': form})

def thanks(request):
    return HttpResponse("Thanks!")

@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def example_game(request):
    context = {'logouturl': '/logout', 'logout':'logout'}
    return render(request, 'gamesite/games/example_game.html', context)


@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def my_view(request):

    if request.user.is_authenticated:

        # Redirect to a success page.
        return HttpResponse("login succeeded")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("login failed")
