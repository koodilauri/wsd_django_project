from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm
import hashlib, random, datetime
from django.core.mail import send_mail
from gamesite.models import UserProfile

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
            if form.cleaned_data['Password'] == form.cleaned_data['Re_enter_Password']:
                # process the data in form.cleaned_data as required
                datas={}
                datas['username']=form.cleaned_data['username']
                datas['email']=form.cleaned_data['email']
                datas['password']=form.cleaned_data['Password']

                #We generate a random activation key
                rnd = str(random.random()).encode('utf8')
                sha = hashlib.sha1(rnd)
                salt = sha.hexdigest()[:5]
                usernamesalt = datas['username']
                string = salt+usernamesalt
                datas['activation_key']= hashlib.sha1(string.encode('utf8')).hexdigest()

                datas['email_path']="templates/ActivationEmail.txt"
                datas['email_subject']="Activate your account"

                #create and save user and profile
                u = User.objects.create_user(username=datas['username'],
                                         email=datas['email'],
                                         password=datas['password'])
                u.is_active = False
                u.save()
                profile=UserProfile()
                profile.user=u
                profile.activation_key=datas['activation_key']
                profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
                profile.save()
                send_mail(datas['email_subject'], profile.activation_key, 'service@example.com', [profile.user.email], fail_silently=False,)
                # redirect to a new URL:
                return HttpResponse('Thank you for registering, an activation key has been sent to your email (check the console Django is runnin)')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, 'gamesite/register.html', {'form': form})

def activation(request, key):
    profile = get_object_or_404(UserProfile, activation_key=key)
    if profile.user.is_active == False:
        profile.user.is_active = True
        profile.user.save()
        return HttpResponse('Username: '+profile.user.username+' has been activated')
    #If user is already active, simply display error message
    else:
        return HttpResponse('already active')
    return HttpResponse('something went wrong with activation')

def new_activation_link(request, username):
    datas={}
    user = get_object_or_404(User, username=username)
    if user is not None and not user.is_active:
        datas['username']=user.username
        datas['email']=user.email

        rnd = str(random.random()).encode('utf8')
        sha = hashlib.sha1(rnd)
        salt = sha.hexdigest()[:5]
        usernamesalt = datas['username']
        string = salt+usernamesalt
        datas['activation_key']= hashlib.sha1(string.encode('utf8')).hexdigest()


        datas['email_path']="/ResendEmail.txt"
        datas['email_subject']="Your new activation key"

        profile = UserProfile.objects.get(user=user)
        profile.activation_key = datas['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()

        send_mail(datas['email_subject'], profile.activation_key, 'service@example.com', [profile.user.email], fail_silently=False,)
        request.session['new_link']=True #Display: new link sent

    return HttpResponseRedirect('/')


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
