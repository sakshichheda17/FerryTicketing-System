from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import PassengerCreationForm, PassengerLoginForm
from django.contrib import messages
from .models import Passenger


def login(request):
	if request.method == "POST":
		form = PassengerLoginForm(request.POST)        
		if form.is_valid():        	
			username = form.cleaned_data.get('username')        	
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)            
			if user is not None:            	
				return redirect('/admin/')           
			else:            	
				if Passenger.objects.filter(username=username,password=password).exists():            		
					messages.success(request, f'The passenger {username} was logged in successfully.')
					passenger_id = Passenger.objects.get(username=username).id
					request.session['username']=username
					return render(request,'select_route.html')

				else:
					messages.warning(request,'Please enter a valid username and password.')

	else:
		form = PassengerLoginForm()


	return render(request,'login.html',{'form': form })


def register(request):
	if request.method == "POST":
		form = PassengerCreationForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data.get('username')
			if Passenger.objects.filter(username=form.cleaned_data['username']).exists():
				# print('Already exists')
				messages.warning(request, f'The username {username} already exists.')

			else:
				form.save()			
				print(form.cleaned_data)
				messages.success(request, f'The passenger {username} was registered successfully.')
				return redirect('login')			    
			
	else:
	    form = PassengerCreationForm()		

	return render(request,'register.html',{'form': form })


def select_route(request):	
	print(request.session['username'])    
	return render(request,'select_route.html')
