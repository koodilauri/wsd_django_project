from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm, PaymentForm, GameForm
import hashlib, random, datetime
from django.core.mail import send_mail
from gamesite.models import UserProfile
from gamesite.models import Game, ScoreBoard
from django.shortcuts import render
from hashlib import md5

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
				datas['activation_key']= 'activate'# hashlib.sha1(string.encode('utf8')).hexdigest()

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
				send_mail(datas['email_subject'], 'activate/'+ profile.activation_key, 'service@example.com', [profile.user.email], fail_silently=False,)
				# redirect to a new URL:
				return HttpResponse('Thank you for registering, an activation key has been sent to your email (check the console Django is runnin)')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = UserForm()

	return render(request, 'gamesite/register.html', {'form': form})

def activation(request, key):
	profile = get_object_or_404(UserProfile, activation_key=key)
	if profile.user.is_active == False:
		fm = "%Y-%m-%d %H:%M:%S"
		exdate = profile.key_expires
		td = exdate.replace(tzinfo=None) - datetime.datetime.now()
		if td.total_seconds() > 0:
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

def submit_score(request):
	if request.method == 'POST':
		s = ScoreBoard(websiteURL = request.POST.get("gameurl"), score = request.POST.get("score"), user = request.user)
		s.save()
		print("jee se toimii")
		print(request.POST.get("gameurl"))
	return HttpResponse('Score submission done!')

@login_required(login_url="/login/")#the view below can only be accessed if user has logged in
def gameview(request, gametitle):
	game = get_object_or_404(Game, websiteURL = gametitle)
	str1 = game.game_url
	score = ScoreBoard.objects.filter(websiteURL = gametitle).order_by('score').reverse()[:5]
	i = str1.index('/', 8)
	context =  {'logouturl': '/logout', 'logout':'logout', 'title': game.title, 'gameurl':game.game_url, 'origin':str1[0:i], 'websiteURL':gametitle, 'score':score}
	return render(request, 'gamesite/game.html', context)

@login_required(login_url="/login/")#the view below can only be accessed if user has logged in
def example_game(request):
	context = {'logouturl': '/logout', 'logout':'logout'}
	return render(request, '/gamesite/games/example_game.html', context)


@login_required(login_url="/login/")#the view below can only be accessed if user has logged in
def my_view(request, username):
	context = {'logouturl': '/logout', 'logout':'logout'}
	form = GameForm()
	return render(request, 'gamesite/account.html', {'form': form})


@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def gameshop(request):
	all_games = Game.objects.all()
	context={
		'all_games' : all_games,
	}
	return render (request, 'gamesite/gameshop.html', context)


@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def game_detail(request, id):
	return HttpResponse("Details for game id:"+ str(id))



@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def payment(request, id):
	if request.method == 'POST':
			form = PaymentForm(request.POST)
			if form.is_valid():
				amount = request.amount
				secret_key = 'd09529cbffa750cc7a4c4c7ed88e49f7'
				pid = request.pid
				sid = request.sid
				checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
				# checksumstr is the string concatenated above
				m = md5(checksumstr.encode("ascii"))
				checksum = m.hexdigest()
				# checksum is the value that should be used in the payment request

				# process the data in form.cleaned_data as required
				post_data = [('pid', pid),('sid',sid),('amount',amount),('success_url','gamesite/payment_success.html'),('cancel_url','gamesite/payment_cancel.html'),('error_url','gamesite/payment_error.html'),('checksum',checksum)]     # a sequence of two element tuples
				result = urllib2.urlopen('http://payments.webcourse.niksula.hut.fi/pay/', urllib.urlencode(post_data))
				content = result.read()
				# redirect to a new URL:
				return render (request, 'gamesite/payment_success.html')

	# if a GET (or any other method) we'll create a blank form

	else:
			g = get_object_or_404(Game, id=id)
			form = PaymentForm()
			pid = "mytestsale"
			sid = g.sid
			amount = g.price
			secret_key = g.skey
			checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
			# checksumstr is the string concatenated above
			m = md5(checksumstr.encode("ascii"))
			checksum = m.hexdigest()
			# checksum is the value that should be used in the payment request
			data = {'form':form,'pid':pid,'sid':sid,'amount':amount,'checksum':checksum}

	return render(request, 'gamesite/payment.html', data)
	# return render (request, 'gamesite/payment.html')




@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def paymentsuccess(request, id=None):
	return render (request, 'gamesite/payment_success.html')

@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def paymentcancel(request, id):
	return render (request, 'gamesite/payment_cancel.html')


@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def paymenterror(request, id):
	return render (request, 'gamesite/payment_error.html')

@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def addgame(request):
    datas={}

    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            datas['title']=form.cleaned_data['title']
            datas['genre']=form.cleaned_data['genre']
            datas['image_url']=form.cleaned_data['image_url']
            datas['game_url']=form.cleaned_data['game_url']
            datas['price']=form.cleaned_data['price']
            datas['websiteURL']=form.cleaned_data['websiteURL']
            datas['sid']=form.cleaned_data['sid']
            datas['skey']=form.cleaned_data['skey']

            g = Game.objects.create(title=datas['title'],
                                        genre = datas['genre'],
                                        image_url = datas['game_url'],
                                        game_url = datas['game_url'],
                                        price = datas['price'],
                                        websiteURL = datas['websiteURL'],
                                        sid = datas['sid'],
                                        skey = datas['skey'])
            g.save()

            return HttpResponse('Thank you for uploading a game!')
    else:
        form = GameForm()

    return render(request, 'gamesite/addgame.html', {'form': form})
