from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm, PaymentForm, GameForm
import hashlib, random, datetime
from django.core.mail import send_mail
from gamesite.models import UserProfile
from gamesite.models import Game, ScoreBoard, Payment, Save
from django.shortcuts import render
from hashlib import md5
from gamesite.models import Payment
from datetime import date
from django.shortcuts import redirect

# Create your views here.

def index(request):
	if request.user.is_authenticated:
		context = {'logouturl': '/logout', 'logout':'logout', 'message':'Welcome'}
		return render(request, "gamesite/index.html", context)
	else:
		context = {'loginurl': '/login', 'login':'login', 'registerurl':'/register', 'register':'register', 'message':'Welcome'}
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
				send_mail(datas['email_subject'], 'activate/'+ profile.activation_key, 'service@example.com', [profile.user.email], fail_silently=False,)
				# redirect to a new URL:
				context = {'loginurl': '/login', 'login':'login', 'registerurl':'/register', 'register':'register', 'message':'Thank you for registering, an activation key has been sent to your email (check the console Django is runnin), on heroku, you cant check console so here is the link: activate/'+ profile.activation_key}
				return render(request, "gamesite/index.html", context)

	# if a GET (or any other method) we'll create a blank form
	else:
		form = UserForm()

	return render(request, 'gamesite/register.html', {'form': form})

def activation(request, key):
	profile = get_object_or_404(UserProfile, activation_key=key)
	context = {'loginurl': '/login', 'login':'login', 'registerurl':'/register', 'register':'register', 'message':'The user is already active'}
	if profile.user.is_active == False:
		fm = "%Y-%m-%d %H:%M:%S"
		exdate = profile.key_expires
		td = exdate.replace(tzinfo=None) - datetime.datetime.now()
		if td.total_seconds() > 0:
			profile.user.is_active = True
			profile.user.save()
			context['message'] = 'Username: '+profile.user.username+' has been activated'
			return render(request, "gamesite/index.html", context)
	#If user is already active, simply display error message
	else:
		return render(request, "gamesite/index.html", context)
	context['message'] = "Something went wrong with activation... Try requesting a new activation key from url /new_activation_link/*yourusername*"
	return render(request, "gamesite/index.html", context)

def new_activation_link(request, username):
	datas={}
	user = get_object_or_404(User, username=username)
	context = {'loginurl': '/login', 'login':'login', 'registerurl':'/register', 'register':'register', 'message':'The user is already active'}
	if user is not None and not user.is_active:
		datas['username']=user.username
		datas['email']=user.email

		#generate a new activation key
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

		send_mail(datas['email_subject'], '/activate'+profile.activation_key, 'service@example.com', [profile.user.email], fail_silently=False,)
		request.session['new_link']=True #Display: new link sent
		context['message'] = 'A new activation key has been sent, check console Django is runnin. link is also provided here since you cant see the console on Heroku: activate/'+profile.activation_key

	return render(request, "gamesite/index.html", context)


def thanks(request):
	return HttpResponse("Thanks!")


def submit_score(request):
	if request.method == 'POST':

		s = ScoreBoard(websiteURL = request.POST.get("gameurl"), score = request.POST.get("score"), user = request.user)
		s.save()
		print("jee se toimii")
		print(request.POST.get("gameurl"))
	return HttpResponse('Score submission done!')

def save(request):
	if request.method == 'POST':
		gameurl = request.POST.get('gameurl')
		game = Game.objects.get(websiteURL=request.POST.get('gameurl'))
		user = request.user
		gameState = request.POST.get('gameState')
		if(Save.objects.filter(game=game, user = user).exists()):
			save = Save.objects.get(game=game,user=user)
			save.gamestate = gameState
			save.save()
		else:
			save = Save(game = game, user=user, gamestate=gameState)
			save.save()
	elif request.method == 'GET':
		game = Game.objects.get(websiteURL=request.GET.get("gameurl"))
		user = request.user
		if(Save.objects.filter(game=game, user=user).exists()):
			save = Save.objects.get(game=game,user=user)
			return HttpResponse(save.gamestate, content_type="text/plain", status=200)
		else:
			return HttpResponse()
	return HttpResponse('/');



@login_required(login_url="/login/")#the view below can only be accessed if user has logged in
def gameview(request, gametitle):
	game = get_object_or_404(Game, websiteURL = gametitle)
	list = Payment.objects.all()
	for i in list:
		if i.pid == request.user.username+'|'+game.websiteURL: #Check if user has made a payment for this game
			if i.result == 'success': #check if the payment is successfull

				#Here we get the origin of the game so we know what messages to accept
				str1 = game.game_url
				score = ScoreBoard.objects.filter(websiteURL = gametitle).order_by('score').reverse()[:5]
				i = str1.index('/', 8)

				context =  {'logouturl': '/logout', 'logout':'logout', 'title': game.title, 'gameurl':game.game_url, 'origin':str1[0:i], 'websiteURL':gametitle, 'score':score}
				return render(request, 'gamesite/game.html', context)

	#If you are the developer, you get automatically access to your game
	if game.developer.username == request.user.username:
		str1 = game.game_url
		score = ScoreBoard.objects.filter(websiteURL = gametitle).order_by('score').reverse()[:5]
		i = str1.index('/', 8)
		context =  {'logouturl': '/logout', 'logout':'logout', 'title': game.title, 'gameurl':game.game_url, 'origin':str1[0:i], 'websiteURL':gametitle, 'score':score}
		return render(request, 'gamesite/game.html', context)

	return redirect('payment', game.id)

@login_required(login_url="/login/")#the view below can only be accessed if user has logged in
def editgame(request, gametitle):
	game = get_object_or_404(Game, websiteURL = gametitle)
	context =  {'logouturl': '/logout', 'logout':'logout', 'title': game.title}
	if request.method == 'GET':
		if game.developer.username == request.user.username:
			#Here we render the initial view when the dev comes to this url
			form = GameForm(initial={'title':game.title, 'websiteURL':'websiteURL cannot be changed', 'game_url':game.game_url, 'price':game.price, 'image_url':game.image_url, 'genre':game.genre})
			form.title = game.title
			context['form'] =  form
			return render(request, 'gamesite/addgame.html', context)
	elif request.method == 'POST':
		#When the dev submits their edited game, we update the game
		form = GameForm(request.POST)
		if form.is_valid():
			game.title = form.cleaned_data['title']
			game.image_url = form.cleaned_data['image_url']
			game.game_url = form.cleaned_data['game_url']
			game.price = form.cleaned_data['price']
			game.genre = form.cleaned_data['genre']
			game.save()
			context['message'] =  'Game updated'
			return render(request, "gamesite/index.html", context)
	return HttpResponse('Unauthorized', status=401) #if you are not the dev, you get this message

@login_required(login_url="/login/")#the view below can only be accessed if user has logged in
def deletegame(request, gametitle):
	game = get_object_or_404(Game, websiteURL = gametitle)
	context =  {'logouturl': '/logout', 'logout':'logout', 'title': game.title}
	if request.method == 'GET':
		#if you are the dev, you need to press a button in the page to delete the game
		if game.developer.username == request.user.username:
			return render(request, 'gamesite/deletegame.html', context)
	elif request.method == 'POST':
		#When the button is pressed, we delete the game
		game.delete()
		context['message'] = "Game: "+game.title+" has been deleted."
		return render(request, "gamesite/index.html", context)
	return HttpResponse('Unauthorized', status=401) #if you are not the dev, you get this message

@login_required(login_url="/login/")#the view below can only be accessed if user has logged in
def example_game(request):
	context = {'logouturl': '/logout', 'logout':'logout'}
	return render(request, '/gamesite/games/example_game.html', context)


@login_required(login_url="/login/")#the view below can only be accessed if user has logged in
def my_view(request):
	context = {'logouturl': '/logout', 'logout':'logout'}
	game = Game.objects.filter(developer = request.user) # we get all the games you have uploaded
	p = Payment.objects.all()
	data = {}
	data['games'] = game
	data['dates'] = ''
	for g in game:
		dates = ''
		for i in p:
			n=i.pid.index('|')
			#For each game, we check any Payments that are successfull and add those to the data dictionary
			if i.pid[n+1:] == g.websiteURL and i.result=='success':
				#the string is in the form of: gameurl|date%gameurl|date%...
				dates += str(g.websiteURL) +'|'+ datetime.datetime.strftime(i.date, "%Y-%m-%d %H:%M:%S") +'%'
		data['dates'] += dates
	data['user']=request.user
	data['dates'] = data['dates'][0:-1] #remove the final % -sign from the string as it is not needed
	return render(request, 'gamesite/account.html', data)


def gameshop(request):
	all_games = Game.objects.all()
	if request.user.is_authenticated:
		list =''
		user = request.user.username
		p=Payment.objects.all()
		for i in p:
			w=i.pid.index('|')
			if i.pid[0:w] == user:
				if i.result == 'success':
						#we check the games the user has bought so the page shows a 'Play' button for them instead of 'Buy'
						list += i.pid[w+1:]+'|'
		list=list[0:-1]
		context={'all_games' : all_games,'logouturl': '/logout', 'logout':'logout', 'boughtgames':list}
	else:
		context={'all_games' : all_games,'loginurl': '/login', 'login':'login', 'registerurl':'/register', 'register':'register'}
	return render (request, 'gamesite/gameshop.html', context)

@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def game_detail(request, id):
	return HttpResponse("Details for game id:"+ str(id))



@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def payment(request, id):
	g = get_object_or_404(Game, id=id)
	if g.developer.username == request.user.username:
		return redirect('gameview', g.websiteURL)
	form = PaymentForm()
	pid = request.user.username+'|'+g.websiteURL
	sid = 'gameshop' #the sites global sid
	amount = g.price
	secret_key = '0a37fc5ef6ecfee9f563ae8d2044b7cd' #the sites global secret key for the payment service
	date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
	checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
	# checksumstr is the string concatenated above
	m = md5(checksumstr.encode("ascii"))
	checksum = m.hexdigest()
	# checksum is the value that should be used in the payment request

	#we check if the user already has a Payment for this game so that we wont create a new one...
	found = False
	list = Payment.objects.all()
	for i in list:
		if i.pid == pid:
			if i.result == 'success':
				return redirect('gameview', g.websiteURL) #if the user has already successfully bought the game, redirect to gamepage
			else:
				i.date = date #update the old Payment object
				found = True
				break
	if not found:
		payment = Payment.objects.create(pid=pid, price = g.price, checksum = checksum, result = 'unfinished', date=date)
		payment.save()
	data = {'form':form,'pid':pid,'sid':sid,'amount':amount,'checksum':checksum}


	return render(request, 'gamesite/payment.html', data)




@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def paymentsuccess(request, id=None):
	#we get the data the payment service sent back
	pid = request.GET.get('pid', '')
	result = request.GET.get('result', '')
	ref = request.GET.get('ref', '')
	checksum = request.GET.get('checksum', '')

	#get the game and payment objects from db
	i = pid.index('|')
	game = get_object_or_404(Game, websiteURL=pid[i+1:])
	secret_key = '0a37fc5ef6ecfee9f563ae8d2044b7cd'
	p = get_object_or_404(Payment, pid=pid)

	#generate checksum from the data we got from payment service
	checksumstr= "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
	m = md5(checksumstr.encode("ascii"))
	checksum2 = m.hexdigest()

	#check if the sums match and update payment object accordingly
	if checksum2 == checksum:
		p.result = result
		p.ref = ref
		p.save()
		return render (request, 'gamesite/payment_success.html')
	return render (request, 'gamesite/payment_error.html')

@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def paymentcancel(request, id=None):
	return render (request, 'gamesite/payment_cancel.html')


@login_required(login_url="/login")#the view below can only be accessed if user has logged in
def paymenterror(request, id=None):
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


            g = Game.objects.create(developer=request.user,
										title=datas['title'],
                                        genre = datas['genre'],
                                        image_url = datas['image_url'],
                                        game_url = datas['game_url'],
                                        price = datas['price'],
                                        websiteURL = datas['websiteURL'])
            g.save()

            return HttpResponseRedirect('/game/'+str(g.websiteURL))
    else:
        form = GameForm()

    return render(request, 'gamesite/addgame.html', {'form': form})
